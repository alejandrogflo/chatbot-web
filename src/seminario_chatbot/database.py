from decimal import Decimal
from typing import Any

import psycopg
from psycopg.rows import dict_row

from seminario_chatbot.ai.models import QueryPlan
from seminario_chatbot.settings import get_settings


# Identificadores y columnas vienen exclusivamente de este mapa constante.
_CATALOGS = {
    "peliculas": {
        "table": "public.peliculas",
        "columns": (
            "id_pelicula",
            "titulo",
            "genero",
            "plataforma",
            "anio_lanzamiento",
            "calificacion",
            "director",
            "actores",
            "productora",
            "duracion_minutos",
            "clasificacion",
        ),
    },
    "videojuegos": {
        "table": "public.videojuegos",
        "columns": (
            "id_videojuego",
            "titulo",
            "genero",
            "plataforma",
            "anio_lanzamiento",
            "calificacion",
            "desarrollador",
            "jugadores",
        ),
    },
}

_GENRE_ALIASES = {
    "disparos": "Shooter",
    "juego de disparos": "Shooter",
    "juegos de disparos": "Shooter",
    "tiros": "Shooter",
    "shooter": "Shooter",
}


class DatabaseConfigurationError(RuntimeError):
    pass


def normalize_genre(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    if not cleaned:
        return None
    return _GENRE_ALIASES.get(cleaned.casefold(), cleaned)


def _json_friendly(row: dict[str, Any]) -> dict[str, Any]:
    result = {}
    for key, value in row.items():
        if isinstance(value, Decimal):
            result[key] = float(value)
        else:
            result[key] = value
    return result


def fetch_catalog(plan: QueryPlan) -> list[dict[str, Any]]:
    """Consulta el catálogo seleccionado con identificadores allowlisted y valores ligados."""
    if plan.categoria not in _CATALOGS:
        raise ValueError("La categoría no es válida.")

    database_url = get_settings().database_url
    if not database_url:
        raise DatabaseConfigurationError("DATABASE_URL no está configurada.")

    catalog = _CATALOGS[plan.categoria]
    filters = ["TRUE"]
    parameters: list[Any] = []

    genre = normalize_genre(plan.genero)
    if genre:
        filters.append("genero ILIKE %s")
        parameters.append(f"%{genre}%")
    if plan.plataforma:
        filters.append("plataforma ILIKE %s")
        parameters.append(f"%{plan.plataforma.strip()}%")
    if plan.titulo:
        filters.append("titulo ILIKE %s")
        parameters.append(f"%{plan.titulo.strip()}%")
    if plan.calificacion_minima is not None:
        operator = ">=" if plan.calificacion_minima_inclusiva else ">"
        filters.append(f"calificacion {operator} %s")
        parameters.append(plan.calificacion_minima)
    if plan.calificacion_maxima is not None:
        operator = "<=" if plan.calificacion_maxima_inclusiva else "<"
        filters.append(f"calificacion {operator} %s")
        parameters.append(plan.calificacion_maxima)
    if plan.anio_desde is not None:
        filters.append("anio_lanzamiento >= %s")
        parameters.append(plan.anio_desde)
    if plan.anio_hasta is not None:
        filters.append("anio_lanzamiento <= %s")
        parameters.append(plan.anio_hasta)

    columns = ", ".join(catalog["columns"])
    where_clause = " AND ".join(filters)
    statement = (
        f"SELECT {columns} FROM {catalog['table']} "
        f"WHERE {where_clause} "
        "ORDER BY calificacion DESC NULLS LAST, titulo ASC LIMIT %s"
    )
    parameters.append(plan.limite)

    try:
        with psycopg.connect(database_url, connect_timeout=5) as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(statement, parameters)
                return [_json_friendly(dict(row)) for row in cursor.fetchall()]
    except psycopg.Error:
        raise
