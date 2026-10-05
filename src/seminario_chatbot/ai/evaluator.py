from typing import Any


def fallback_answer(categoria: str, records: list[dict[str, Any]]) -> str:
    etiqueta = "películas" if categoria == "peliculas" else "videojuegos"
    if not records:
        return f"No encontré {etiqueta} que coincidan con esos filtros."

    lines = [f"Encontré {len(records)} {etiqueta} en el catálogo:"]
    for row in records:
        details = [row.get("genero"), row.get("plataforma")]
        year = row.get("anio_lanzamiento")
        rating = row.get("calificacion")
        if year is not None:
            details.append(str(year))
        if rating is not None:
            details.append(f"calificación {rating:g}/10")
        suffix = f" — {', '.join(str(item) for item in details if item)}" if any(details) else ""
        lines.append(f"• {row['titulo']}{suffix}")
    return "\n".join(lines)


def evaluate_grounding(
    answer: str,
    categoria: str,
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    """Regla determinista: la respuesta debe citar todos los títulos recuperados."""
    if not records:
        return {
            "passed": True,
            "score": 1.0,
            "checks": ["sin_resultados_no_afirma_titulos"],
            "fallback_used": False,
        }

    normalized_answer = answer.casefold()
    missing_titles = [
        str(row["titulo"])
        for row in records
        if str(row["titulo"]).casefold() not in normalized_answer
    ]
    if not missing_titles:
        return {
            "passed": True,
            "score": 1.0,
            "checks": ["incluye_todos_los_titulos_recuperados"],
            "fallback_used": False,
        }

    return {
        "passed": False,
        "score": 0.0,
        "checks": ["faltan_titulos_recuperados"],
        "missing_titles": missing_titles,
        "fallback_used": True,
        "answer": fallback_answer(categoria, records),
    }
