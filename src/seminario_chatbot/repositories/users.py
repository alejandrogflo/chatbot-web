"""Consultas parametrizadas para las cuentas de usuario."""

import psycopg
from psycopg.rows import dict_row

from seminario_chatbot.database import DatabaseConfigurationError
from seminario_chatbot.settings import get_settings


class InitialAdminAlreadyExists(RuntimeError):
    """Indica que el aprovisionamiento inicial ya se realizó."""


class EmailAlreadyExists(RuntimeError):
    """Indica que el correo ya pertenece a otra cuenta."""


def _connect() -> psycopg.Connection:
    database_url = get_settings().database_url
    if not database_url:
        raise DatabaseConfigurationError("DATABASE_URL no está configurada.")
    return psycopg.connect(database_url, connect_timeout=5, row_factory=dict_row)


def find_user_by_email(email: str) -> dict | None:
    with _connect() as connection:
        return connection.execute(
            """
            SELECT id_usuario, nombre, correo, password_hash, rol
            FROM public.usuarios
            WHERE LOWER(correo) = LOWER(%s)
            """,
            (email,),
        ).fetchone()


def find_user_by_id(user_id: int) -> dict | None:
    with _connect() as connection:
        return connection.execute(
            """
            SELECT id_usuario, nombre, correo, rol
            FROM public.usuarios
            WHERE id_usuario = %s
            """,
            (user_id,),
        ).fetchone()


def create_initial_admin(name: str, email: str, password_hash: str) -> int:
    """Crea el primer administrador bajo un bloqueo transaccional."""
    try:
        with _connect() as connection:
            # Evita que dos ejecuciones simultáneas creen administradores iniciales.
            connection.execute("SELECT pg_advisory_xact_lock(%s)", (741020261004,))
            has_admin = connection.execute(
                "SELECT EXISTS (SELECT 1 FROM public.usuarios WHERE rol = 'admin')"
            ).fetchone()["exists"]
            if has_admin:
                raise InitialAdminAlreadyExists

            row = connection.execute(
                """
                INSERT INTO public.usuarios (nombre, correo, password_hash, rol)
                VALUES (%s, %s, %s, 'admin')
                RETURNING id_usuario
                """,
                (name, email, password_hash),
            ).fetchone()
            return row["id_usuario"]
    except psycopg.errors.UniqueViolation as exc:
        raise EmailAlreadyExists from exc
