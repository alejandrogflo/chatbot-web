"""Agregados privados del consumo de IA."""

import psycopg
from psycopg.rows import dict_row

from seminario_chatbot.database import DatabaseConfigurationError
from seminario_chatbot.settings import get_settings


def _connect() -> psycopg.Connection:
    database_url = get_settings().database_url
    if not database_url:
        raise DatabaseConfigurationError("DATABASE_URL no está configurada.")
    return psycopg.connect(database_url, connect_timeout=5, row_factory=dict_row)


def summarize_user_consumption(user_id: int) -> list[dict]:
    """Suma los consumos asociados exclusivamente al usuario indicado."""
    with _connect() as connection:
        return list(
            connection.execute(
                """
                SELECT
                    categoria,
                    COUNT(*) AS consultas,
                    COALESCE(SUM(tokens), 0) AS tokens_palabras,
                    COALESCE(SUM(tokens_proveedor), 0) AS tokens_proveedor
                FROM public.consumo_tokens
                WHERE id_usuario = %s
                GROUP BY categoria
                """,
                (user_id,),
            ).fetchall()
        )
