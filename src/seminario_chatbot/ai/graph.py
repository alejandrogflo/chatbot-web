from functools import lru_cache
import logging
import time
from operator import add
from typing import Annotated, Any, Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from seminario_chatbot.ai.evaluator import evaluate_grounding, fallback_answer
from seminario_chatbot.ai.models import QueryPlan
from seminario_chatbot.ai.planner import (
    AIConfigurationError,
    draft_answer,
    extract_query_plan,
)
from seminario_chatbot.database import DatabaseConfigurationError, fetch_catalog

logger = logging.getLogger(__name__)


class MovieGameState(TypedDict, total=False):
    question: str
    plan: dict[str, Any] | None
    categoria: str | None
    records: list[dict[str, Any]]
    answer: str
    error_code: str | None
    error_message: str | None
    evaluation: dict[str, Any]
    usage: list[dict[str, Any]]
    tokens_palabras: int
    tokens_proveedor: int
    trace: Annotated[list[dict[str, Any]], add]


def _plan_node(state: MovieGameState, *, model: Any | None = None) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        plan, usage = extract_query_plan(state["question"], model=model)
    except AIConfigurationError as exc:
        return {
            "error_code": "ai_not_configured",
            "error_message": str(exc),
            "trace": [_trace_event("planificar", "error", started)],
        }
    except Exception:
        logger.exception("No se pudo interpretar la pregunta con el proveedor de IA.")
        return {
            "error_code": "ai_request_failed",
            "error_message": "No se pudo interpretar la consulta con el modelo de IA.",
            "trace": [_trace_event("planificar", "error", started)],
        }

    return {
        "plan": plan.model_dump(),
        "categoria": plan.categoria,
        "usage": [usage],
        "tokens_palabras": usage["palabras"],
        "tokens_proveedor": usage["total_tokens"],
        "trace": [_trace_event("planificar", "ok", started)],
    }


def _after_plan(state: MovieGameState) -> Literal["clarify", "query", "error"]:
    if state.get("error_code"):
        return "error"
    plan_data = state.get("plan")
    if not plan_data or not plan_data.get("categoria"):
        return "clarify"
    return "query"


def _clarify_node(_: MovieGameState) -> dict[str, Any]:
    return {
        "answer": "¿Buscas películas o videojuegos? Indica la categoría y, si quieres, un género o calificación mínima.",
        "evaluation": {
            "passed": True,
            "score": 1.0,
            "checks": ["solicita_categoria_ambigua"],
            "fallback_used": False,
        },
        "trace": [{"node": "aclarar", "status": "ok", "elapsed_ms": 0}],
    }


def _query_node(
    state: MovieGameState,
    *,
    catalog_query=fetch_catalog,
) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        plan = QueryPlan.model_validate(state["plan"])
        records = catalog_query(plan)
    except DatabaseConfigurationError as exc:
        return {
            "error_code": "database_not_configured",
            "error_message": str(exc),
            "trace": [_trace_event("consultar_postgres", "error", started)],
        }
    except Exception:
        logger.exception("No se pudo consultar el catálogo PostgreSQL.")
        return {
            "error_code": "database_query_failed",
            "error_message": "No se pudo consultar el catálogo PostgreSQL.",
            "trace": [_trace_event("consultar_postgres", "error", started)],
        }
    return {
        "records": records,
        "trace": [_trace_event("consultar_postgres", "ok", started, rows=len(records))],
    }


def _after_query(state: MovieGameState) -> Literal["answer", "error"]:
    return "error" if state.get("error_code") else "answer"


def _answer_node(state: MovieGameState, *, model: Any | None = None) -> dict[str, Any]:
    started = time.perf_counter()
    categoria = state["categoria"] or "peliculas"
    records = state.get("records", [])
    if not records:
        return {
            "answer": fallback_answer(categoria, records),
            "trace": [_trace_event("redactar", "sin_resultados", started)],
        }

    try:
        answer, usage = draft_answer(
            state["question"], categoria, records, model=model
        )
    except AIConfigurationError as exc:
        return {
            "answer": fallback_answer(categoria, records),
            "error_code": "ai_not_configured_for_answer",
            "error_message": str(exc),
            "trace": [_trace_event("redactar", "respaldo", started)],
        }
    except Exception:
        logger.exception("Falló la redacción con IA; se usará la respuesta del catálogo.")
        return {
            "answer": fallback_answer(categoria, records),
            "error_code": "ai_answer_fallback",
            "error_message": "La respuesta de IA falló; se mostraron los datos del catálogo.",
            "trace": [_trace_event("redactar", "respaldo", started)],
        }

    return {
        "answer": answer,
        "usage": state.get("usage", []) + [usage],
        "tokens_palabras": state.get("tokens_palabras", 0) + usage["palabras"],
        "tokens_proveedor": state.get("tokens_proveedor", 0) + usage["total_tokens"],
        "trace": [_trace_event("redactar", "ok", started)],
    }


def _evaluate_node(state: MovieGameState) -> dict[str, Any]:
    started = time.perf_counter()
    result = evaluate_grounding(
        state.get("answer", ""),
        state.get("categoria") or "peliculas",
        state.get("records", []),
    )
    event_status = "respaldo" if result.get("fallback_used") else "ok"
    event = _trace_event("evaluar_fundamentacion", event_status, started)
    if result.get("fallback_used"):
        return {"answer": result.pop("answer"), "evaluation": result, "trace": [event]}
    return {"evaluation": result, "trace": [event]}


def _error_node(state: MovieGameState) -> dict[str, Any]:
    messages = {
        "ai_not_configured": "Falta configurar GROQ_API_KEY en el archivo local .env.",
        "ai_request_failed": "No pude interpretar la pregunta con el modelo. Inténtalo de nuevo.",
        "database_not_configured": "Falta configurar DATABASE_URL en el archivo local .env.",
        "database_query_failed": "No pude consultar PostgreSQL. Revisa la conexión y vuelve a intentar.",
    }
    code = state.get("error_code", "ai_request_failed")
    return {
        "answer": messages.get(code, "No se pudo completar la consulta."),
        "evaluation": {
            "passed": False,
            "score": 0.0,
            "checks": [code],
            "fallback_used": False,
        },
        "trace": [{"node": "manejar_error", "status": "error", "elapsed_ms": 0}],
    }


def _trace_event(node: str, status: str, started: float, **details: Any) -> dict[str, Any]:
    return {
        "node": node,
        "status": status,
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 1),
        **details,
    }


def build_chat_graph(
    *,
    model: Any | None = None,
    catalog_query=fetch_catalog,
):
    """Construye el workflow; no instala un checkpointer ni retiene estado entre preguntas."""

    def plan_node(state: MovieGameState):
        return _plan_node(state, model=model)

    def query_node(state: MovieGameState):
        return _query_node(state, catalog_query=catalog_query)

    def answer_node(state: MovieGameState):
        return _answer_node(state, model=model)

    workflow = StateGraph(MovieGameState)
    workflow.add_node("planificar", plan_node)
    workflow.add_node("aclarar", _clarify_node)
    workflow.add_node("consultar_postgres", query_node)
    workflow.add_node("redactar", answer_node)
    workflow.add_node("evaluar_fundamentacion", _evaluate_node)
    workflow.add_node("manejar_error", _error_node)

    workflow.add_edge(START, "planificar")
    workflow.add_conditional_edges(
        "planificar",
        _after_plan,
        {"clarify": "aclarar", "query": "consultar_postgres", "error": "manejar_error"},
    )
    workflow.add_conditional_edges(
        "consultar_postgres",
        _after_query,
        {"answer": "redactar", "error": "manejar_error"},
    )
    workflow.add_edge("redactar", "evaluar_fundamentacion")
    workflow.add_edge("aclarar", END)
    workflow.add_edge("manejar_error", END)
    workflow.add_edge("evaluar_fundamentacion", END)
    return workflow.compile()


@lru_cache(maxsize=1)
def get_chat_graph():
    """Crea una instancia reutilizable; las invocaciones conservan estado independiente."""
    return build_chat_graph()


def run_chat(question: str) -> MovieGameState:
    cleaned = question.strip()
    if not cleaned:
        raise ValueError("Escribe una pregunta.")
    if len(cleaned) > 500:
        raise ValueError("La pregunta no puede superar 500 caracteres.")
    initial_state: MovieGameState = {
        "question": cleaned,
        "usage": [],
        "tokens_palabras": 0,
        "tokens_proveedor": 0,
        "trace": [],
    }
    return get_chat_graph().invoke(initial_state)


def graph_mermaid() -> str:
    return build_chat_graph().get_graph().draw_mermaid()
