"""Consultas parametrizadas para las cuentas de usuario."""

import psycopg
from psycopg.rows import dict_row

from seminario_chatbot.database import DatabaseConfigurationError
from seminario_chatbot.settings import get_settings


class InitialAdminAlreadyExists(RuntimeError):
    """Indica que el aprovisionamiento inicial ya se realizó."""


class EmailAlreadyExists(RuntimeError):
    """Indica que el correo ya pertenece a otra cuenta."""


class UserNotFound(RuntimeError):
    """Indica que la cuenta que se iba a modificar ya no existe."""


class LastAdminProtected(RuntimeError):
    """Indica que la operación quitaría la última cuenta administradora."""


class SelfAccountDeleteBlocked(RuntimeError):
    """Indica que un administrador intentó eliminar su propia cuenta."""


class SelfAdminRoleChangeBlocked(RuntimeError):
    """Indica que un administrador intentó quitarse su propio rol."""


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


def list_users() -> list[dict]:
    """Lista campos de cuenta visibles para administración, nunca el hash."""
    with _connect() as connection:
        return list(
            connection.execute(
                """
                SELECT id_usuario, nombre, correo, rol, fecha_registro
                FROM public.usuarios
                ORDER BY fecha_registro DESC, id_usuario DESC
                """
            ).fetchall()
        )


def find_user_for_admin(user_id: int) -> dict | None:
    """Busca los campos editables de una cuenta sin leer su hash."""
    with _connect() as connection:
        return connection.execute(
            """
            SELECT id_usuario, nombre, correo, rol, fecha_registro
            FROM public.usuarios
            WHERE id_usuario = %s
            """,
            (user_id,),
        ).fetchone()


def create_user(name: str, email: str, password_hash: str, role: str) -> int:
    """Crea una cuenta administrativa respetando la unicidad de correo."""
    try:
        with _connect() as connection:
            # Serializa altas y bajas para proteger la última cuenta admin.
            connection.execute("LOCK TABLE public.usuarios IN SHARE ROW EXCLUSIVE MODE")
            row = connection.execute(
                """
                INSERT INTO public.usuarios (nombre, correo, password_hash, rol)
                VALUES (%s, %s, %s, %s)
                RETURNING id_usuario
                """,
                (name, email, password_hash, role),
            ).fetchone()
            return row["id_usuario"]
    except psycopg.errors.UniqueViolation as exc:
        raise EmailAlreadyExists from exc


def update_user(
    user_id: int,
    actor_user_id: int,
    name: str,
    email: str,
    role: str,
    password_hash: str | None,
) -> None:
    """Actualiza una cuenta; un hash nulo significa conservar la contraseña."""
    try:
        with _connect() as connection:
            connection.execute("LOCK TABLE public.usuarios IN SHARE ROW EXCLUSIVE MODE")
            current = connection.execute(
                """
                SELECT id_usuario, rol
                FROM public.usuarios
                WHERE id_usuario = %s
                FOR UPDATE
                """,
                (user_id,),
            ).fetchone()
            if current is None:
                raise UserNotFound

            if (
                user_id == actor_user_id
                and current["rol"] == "admin"
                and role != "admin"
            ):
                raise SelfAdminRoleChangeBlocked
            if current["rol"] == "admin" and role != "admin":
                admin_count = connection.execute(
                    "SELECT COUNT(*) AS total FROM public.usuarios WHERE rol = 'admin'"
                ).fetchone()["total"]
                if admin_count <= 1:
                    raise LastAdminProtected

            if password_hash is None:
                statement = """
                    UPDATE public.usuarios
                    SET nombre = %s, correo = %s, rol = %s
                    WHERE id_usuario = %s
                    """
                parameters = (name, email, role, user_id)
            else:
                statement = """
                    UPDATE public.usuarios
                    SET nombre = %s, correo = %s, rol = %s, password_hash = %s
                    WHERE id_usuario = %s
                    """
                parameters = (name, email, role, password_hash, user_id)
            connection.execute(statement, parameters)
    except psycopg.errors.UniqueViolation as exc:
        raise EmailAlreadyExists from exc


def delete_user(user_id: int, actor_user_id: int) -> None:
    """Elimina una cuenta excepto la propia o la última cuenta administradora."""
    with _connect() as connection:
        connection.execute("LOCK TABLE public.usuarios IN SHARE ROW EXCLUSIVE MODE")
        current = connection.execute(
            """
            SELECT id_usuario, rol
            FROM public.usuarios
            WHERE id_usuario = %s
            FOR UPDATE
            """,
            (user_id,),
        ).fetchone()
        if current is None:
            raise UserNotFound
        if user_id == actor_user_id:
            raise SelfAccountDeleteBlocked
        if current["rol"] == "admin":
            admin_count = connection.execute(
                "SELECT COUNT(*) AS total FROM public.usuarios WHERE rol = 'admin'"
            ).fetchone()["total"]
            if admin_count <= 1:
                raise LastAdminProtected
        connection.execute(
            "DELETE FROM public.usuarios WHERE id_usuario = %s",
            (user_id,),
        )


def create_initial_admin(name: str, email: str, password_hash: str) -> int:
    """Crea el primer administrador bajo un bloqueo transaccional."""
    try:
        with _connect() as connection:
            # Evita que dos ejecuciones simultáneas creen administradores iniciales.
            connection.execute("SELECT pg_advisory_xact_lock(%s)", (741020261004,))
            # Coordina el aprovisionamiento con altas/bajas administrativas de F-002.
            connection.execute("LOCK TABLE public.usuarios IN SHARE ROW EXCLUSIVE MODE")
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
