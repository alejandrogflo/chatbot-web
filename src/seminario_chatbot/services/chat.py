"""Coordinación del grafo de consulta y persistencia del historial."""

from typing import Any

from seminario_chatbot.ai.graph import run_chat
from seminario_chatbot.repositories.conversations import save_exchange


class ChatProcessingError(RuntimeError):
    """La ejecución del grafo no produjo una respuesta persistible."""


def _non_negative_count(value: Any) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError, OverflowError):
        return 0


def process_question(user_id: int, question: str) -> dict[str, Any]:
    """Ejecuta una consulta independiente y guarda la pregunta y su respuesta."""
    result = run_chat(question)
    answer = result.get("answer")
    if not isinstance(answer, str) or not answer.strip():
        raise ChatProcessingError("El grafo no devolvió una respuesta.")

    normalized_answer = answer.strip()
    category = result.get("categoria")
    if category not in {"peliculas", "videojuegos"}:
        category = None
    academic_tokens = _non_negative_count(result.get("tokens_palabras", 0))
    provider_tokens = _non_negative_count(result.get("tokens_proveedor", 0))
    conversation_id = save_exchange(
        user_id,
        question,
        normalized_answer,
        category=category,
        academic_tokens=academic_tokens,
        provider_tokens=provider_tokens,
    )
    return {
        "id_conversacion": conversation_id,
        "respuesta": normalized_answer,
        "categoria": category,
        "tokens_palabras": academic_tokens,
        "tokens_proveedor": provider_tokens,
        "error_code": result.get("error_code"),
        "evaluation": result.get("evaluation", {}),
    }
