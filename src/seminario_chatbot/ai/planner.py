import json
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from seminario_chatbot.ai.models import QueryPlan
from seminario_chatbot.ai.prompts import ANSWER_SYSTEM_PROMPT, PLANNER_SYSTEM_PROMPT
from seminario_chatbot.ai.usage import count_words, provider_token_usage
from seminario_chatbot.settings import get_settings


class AIConfigurationError(RuntimeError):
    pass


def create_chat_model() -> ChatGroq:
    settings = get_settings()
    if not settings.groq_api_key:
        raise AIConfigurationError(
            "GROQ_API_KEY no está configurada. Agrégala al archivo local .env."
        )
    return ChatGroq(
        model=settings.groq_model,
        temperature=0,
        reasoning_format="hidden",
        api_key=settings.groq_api_key,
    )


def extract_query_plan(
    question: str,
    *,
    model: Any | None = None,
) -> tuple[QueryPlan, dict[str, Any]]:
    chat_model = model or create_chat_model()
    planner = chat_model.with_structured_output(
        QueryPlan,
        method="function_calling",
        include_raw=True,
    )
    result = planner.invoke(
        [
            SystemMessage(content=PLANNER_SYSTEM_PROMPT),
            HumanMessage(content=question),
        ]
    )
    plan = result.get("parsed")
    raw = result.get("raw")
    if not isinstance(plan, QueryPlan):
        raise ValueError("El modelo no devolvió un plan de consulta válido.")

    plan_text = plan.model_dump_json(exclude_none=False)
    usage = provider_token_usage(raw)
    usage.update(
        {
            "operation": "planificador",
            "palabras": count_words(PLANNER_SYSTEM_PROMPT)
            + count_words(question)
            + count_words(plan_text),
            "model": get_settings().groq_model,
        }
    )
    return plan, usage


def draft_answer(
    question: str,
    categoria: str,
    records: list[dict[str, Any]],
    *,
    model: Any | None = None,
) -> tuple[str, dict[str, Any]]:
    chat_model = model or create_chat_model()
    evidence = json.dumps(records, ensure_ascii=False, default=str)
    user_content = (
        f"Categoría: {categoria}\n"
        f"Pregunta: {question}\n"
        f"Filas recuperadas del catálogo (JSON):\n{evidence}"
    )
    messages = [
        SystemMessage(content=ANSWER_SYSTEM_PROMPT),
        HumanMessage(content=user_content),
    ]
    response = chat_model.invoke(messages)
    answer = str(response.content).strip()
    prompt_text = "\n".join(str(message.content) for message in messages)
    usage = provider_token_usage(response)
    usage.update(
        {
            "operation": "redactor",
            "palabras": count_words(prompt_text) + count_words(answer),
            "model": get_settings().groq_model,
        }
    )
    return answer, usage
