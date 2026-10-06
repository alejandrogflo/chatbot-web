"""Coordinación del grafo de consulta y persistencia del historial."""

from typing import Any

from seminario_chatbot.ai.graph import run_chat
from seminario_chatbot.repositories.conversations import save_exchange


class ChatProcessingError(RuntimeError):
    """La ejecución del grafo no produjo una respuesta persistible."""


def process_question(user_id: int, question: str) -> dict[str, Any]:
    """Ejecuta una consulta independiente y guarda la pregunta y su respuesta."""
    result = run_chat(question)
    answer = result.get("answer")
    if not isinstance(answer, str) or not answer.strip():
        raise ChatProcessingError("El grafo no devolvió una respuesta.")

    normalized_answer = answer.strip()
    conversation_id = save_exchange(user_id, question, normalized_answer)
    return {
        "id_conversacion": conversation_id,
        "respuesta": normalized_answer,
        "categoria": result.get("categoria"),
        "tokens_palabras": result.get("tokens_palabras", 0),
        "tokens_proveedor": result.get("tokens_proveedor", 0),
        "error_code": result.get("error_code"),
        "evaluation": result.get("evaluation", {}),
    }
