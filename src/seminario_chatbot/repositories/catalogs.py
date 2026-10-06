"""Consultas parametrizadas para los catálogos existentes."""

from decimal import Decimal

import psycopg
from psycopg.rows import dict_row

from seminario_chatbot.database import DatabaseConfigurationError
from seminario_chatbot.settings import get_settings


class CatalogItemNotFound(RuntimeError):
    """Indica que el registro de catálogo ya no existe."""


_CATALOGS = {
    "peliculas": {
        "label": "Películas",
        "singular": "película",
        "table": "public.peliculas",
        "id_column": "id_pelicula",
        "list_fields": ("titulo", "genero", "plataforma", "anio_lanzamiento", "calificacion"),
        "fields": (
            {"name": "titulo", "label": "Título", "kind": "text", "max_length": 150, "required": True},
            {"name": "genero", "label": "Género", "kind": "text", "max_length": 100},
            {"name": "plataforma", "label": "Plataforma", "kind": "text", "max_length": 100},
            {"name": "anio_lanzamiento", "label": "Año de lanzamiento", "kind": "integer", "min": 0, "max": 2147483647, "step": 1},
            {"name": "calificacion", "label": "Calificación (0–10)", "kind": "decimal", "min": 0, "max": 10, "step": "0.1"},
            {"name": "director", "label": "Director", "kind": "text", "max_length": 150},
            {"name": "actores", "label": "Actores", "kind": "textarea"},
            {"name": "productora", "label": "Productora", "kind": "text", "max_length": 150},
            {"name": "duracion_minutos", "label": "Duración (minutos)", "kind": "integer", "min": 0, "max": 2147483647, "step": 1},
            {"name": "clasificacion", "label": "Clasificación", "kind": "text", "max_length": 20},
        ),
    },
    "videojuegos": {
        "label": "Videojuegos",
        "singular": "videojuego",
        "table": "public.videojuegos",
        "id_column": "id_videojuego",
        "list_fields": ("titulo", "genero", "plataforma", "anio_lanzamiento", "calificacion"),
        "fields": (
            {"name": "titulo", "label": "Título", "kind": "text", "max_length": 150, "required": True},
            {"name": "genero", "label": "Género", "kind": "text", "max_length": 100},
            {"name": "plataforma", "label": "Plataforma", "kind": "text", "max_length": 100},
            {"name": "anio_lanzamiento", "label": "Año de lanzamiento", "kind": "integer", "min": 0, "max": 2147483647, "step": 1},
            {"name": "calificacion", "label": "Calificación (0–10)", "kind": "decimal", "min": 0, "max": 10, "step": "0.1"},
            {"name": "desarrollador", "label": "Desarrollador", "kind": "text", "max_length": 150},
            {"name": "jugadores", "label": "Jugadores", "kind": "text", "max_length": 50},
        ),
    },
}


def get_catalog_definition(catalog_key: str) -> dict | None:
    """Devuelve la definición interna para una de las dos tablas permitidas."""
    return _CATALOGS.get(catalog_key)


def _definition(catalog_key: str) -> dict:
    definition = get_catalog_definition(catalog_key)
    if definition is None:
        raise ValueError("El catálogo solicitado no es válido.")
    return definition


def _connect() -> psycopg.Connection:
    database_url = get_settings().database_url
    if not database_url:
        raise DatabaseConfigurationError("DATABASE_URL no está configurada.")
    return psycopg.connect(database_url, connect_timeout=5, row_factory=dict_row)


def list_catalog_items(catalog_key: str) -> list[dict]:
    definition = _definition(catalog_key)
    id_column = definition["id_column"]
    columns = (id_column, *definition["list_fields"])
    statement = (
        f"SELECT {', '.join(columns)} FROM {definition['table']} "
        f"ORDER BY titulo ASC, {id_column} ASC"
    )
    with _connect() as connection:
        return list(connection.execute(statement).fetchall())


def find_catalog_item(catalog_key: str, item_id: int) -> dict | None:
    definition = _definition(catalog_key)
    columns = (definition["id_column"], *(field["name"] for field in definition["fields"]))
    statement = (
        f"SELECT {', '.join(columns)} FROM {definition['table']} "
        f"WHERE {definition['id_column']} = %s"
    )
    with _connect() as connection:
        return connection.execute(statement, (item_id,)).fetchone()


def create_catalog_item(catalog_key: str, values: dict) -> int:
    definition = _definition(catalog_key)
    columns = tuple(field["name"] for field in definition["fields"])
    placeholders = ", ".join("%s" for _ in columns)
    statement = (
        f"INSERT INTO {definition['table']} ({', '.join(columns)}) "
        f"VALUES ({placeholders}) RETURNING {definition['id_column']}"
    )
    parameters = tuple(values[column] for column in columns)
    with _connect() as connection:
        row = connection.execute(statement, parameters).fetchone()
        return row[definition["id_column"]]


def update_catalog_item(catalog_key: str, item_id: int, values: dict) -> None:
    definition = _definition(catalog_key)
    columns = tuple(field["name"] for field in definition["fields"])
    assignments = ", ".join(f"{column} = %s" for column in columns)
    statement = (
        f"UPDATE {definition['table']} SET {assignments} "
        f"WHERE {definition['id_column']} = %s "
        f"RETURNING {definition['id_column']}"
    )
    parameters = (*(values[column] for column in columns), item_id)
    with _connect() as connection:
        row = connection.execute(statement, parameters).fetchone()
        if row is None:
            raise CatalogItemNotFound


def delete_catalog_item(catalog_key: str, item_id: int) -> None:
    definition = _definition(catalog_key)
    statement = (
        f"DELETE FROM {definition['table']} "
        f"WHERE {definition['id_column']} = %s "
        f"RETURNING {definition['id_column']}"
    )
    with _connect() as connection:
        row = connection.execute(statement, (item_id,)).fetchone()
        if row is None:
            raise CatalogItemNotFound
