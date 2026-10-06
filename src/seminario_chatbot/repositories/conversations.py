"""Persistencia de conversaciones y lecturas aisladas por cuenta."""

import psycopg
from psycopg.rows import dict_row

from seminario_chatbot.database import DatabaseConfigurationError
from seminario_chatbot.settings import get_settings


def _connect() -> psycopg.Connection:
    database_url = get_settings().database_url
    if not database_url:
        raise DatabaseConfigurationError("DATABASE_URL no está configurada.")
    return psycopg.connect(database_url, connect_timeout=5, row_factory=dict_row)


def save_exchange(user_id: int, question: str, answer: str) -> int:
    """Guarda una consulta independiente y sus dos mensajes en una transacción."""
    with _connect() as connection:
        conversation = connection.execute(
            """
            INSERT INTO public.conversaciones (id_usuario)
            VALUES (%s)
            RETURNING id_conversacion
            """,
            (user_id,),
        ).fetchone()
        conversation_id = conversation["id_conversacion"]
        connection.execute(
            """
            INSERT INTO public.mensajes (id_conversacion, rol, contenido)
            VALUES (%s, 'usuario', %s), (%s, 'asistente', %s)
            """,
            (conversation_id, question, conversation_id, answer),
        )
        return conversation_id


def list_user_conversations(user_id: int) -> list[dict]:
    """Lista preguntas y respuestas pertenecientes solo a la cuenta indicada."""
    with _connect() as connection:
        return list(
            connection.execute(
                """
                SELECT
                    c.id_conversacion,
                    c.fecha_creacion,
                    (
                        SELECT m.contenido
                        FROM public.mensajes AS m
                        WHERE m.id_conversacion = c.id_conversacion
                          AND m.rol = 'usuario'
                        ORDER BY m.fecha, m.id_mensaje
                        LIMIT 1
                    ) AS pregunta,
                    (
                        SELECT m.contenido
                        FROM public.mensajes AS m
                        WHERE m.id_conversacion = c.id_conversacion
                          AND m.rol = 'asistente'
                        ORDER BY m.fecha, m.id_mensaje
                        LIMIT 1
                    ) AS respuesta
                FROM public.conversaciones AS c
                WHERE c.id_usuario = %s
                  AND EXISTS (
                      SELECT 1 FROM public.mensajes AS m
                      WHERE m.id_conversacion = c.id_conversacion
                        AND m.rol = 'usuario'
                  )
                  AND EXISTS (
                      SELECT 1 FROM public.mensajes AS m
                      WHERE m.id_conversacion = c.id_conversacion
                        AND m.rol = 'asistente'
                  )
                ORDER BY c.fecha_creacion DESC, c.id_conversacion DESC
                """,
                (user_id,),
            ).fetchall()
        )


def find_user_conversation(user_id: int, conversation_id: int) -> dict | None:
    """Busca una conversación propia; las de otras cuentas no son visibles."""
    with _connect() as connection:
        return connection.execute(
            """
            SELECT
                c.id_conversacion,
                c.fecha_creacion,
                (
                    SELECT m.contenido
                    FROM public.mensajes AS m
                    WHERE m.id_conversacion = c.id_conversacion
                      AND m.rol = 'usuario'
                    ORDER BY m.fecha, m.id_mensaje
                    LIMIT 1
                ) AS pregunta,
                (
                    SELECT m.contenido
                    FROM public.mensajes AS m
                    WHERE m.id_conversacion = c.id_conversacion
                      AND m.rol = 'asistente'
                    ORDER BY m.fecha, m.id_mensaje
                    LIMIT 1
                ) AS respuesta
            FROM public.conversaciones AS c
            WHERE c.id_usuario = %s
              AND c.id_conversacion = %s
              AND EXISTS (
                  SELECT 1 FROM public.mensajes AS m
                  WHERE m.id_conversacion = c.id_conversacion
                    AND m.rol = 'usuario'
              )
              AND EXISTS (
                  SELECT 1 FROM public.mensajes AS m
                  WHERE m.id_conversacion = c.id_conversacion
                    AND m.rol = 'asistente'
              )
            """,
            (user_id, conversation_id),
        ).fetchone()
