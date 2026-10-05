import re
from typing import Any


_WORD_RE = re.compile(r"[\w]+(?:['’\-][\w]+)*", flags=re.UNICODE)


def count_words(text: str) -> int:
    """Conteo académico: cada palabra visible equivale a un token."""
    return len(_WORD_RE.findall(text))


def provider_token_usage(message: Any) -> dict[str, int]:
    metadata = getattr(message, "response_metadata", {}) or {}
    usage = metadata.get("token_usage", {}) or {}
    return {
        "prompt_tokens": int(usage.get("prompt_tokens", 0) or 0),
        "completion_tokens": int(usage.get("completion_tokens", 0) or 0),
        "total_tokens": int(usage.get("total_tokens", 0) or 0),
    }
