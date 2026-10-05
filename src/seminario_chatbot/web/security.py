"""Protecciones de sesión, CSRF y autorización para rutas Flask."""

from functools import wraps
import hmac
import secrets

import psycopg
from flask import abort, current_app, g, redirect, request, session, url_for

from seminario_chatbot.database import DatabaseConfigurationError
from seminario_chatbot.repositories.users import find_user_by_id


_MUTATING_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def csrf_token() -> str:
    token = session.get("_csrf_token")
    if token is None:
        token = secrets.token_urlsafe(32)
        session["_csrf_token"] = token
    return token


def validate_csrf() -> None:
    expected = session.get("_csrf_token")
    submitted = request.form.get("csrf_token", "")
    if not expected or not submitted or not hmac.compare_digest(expected, submitted):
        abort(400)


def csrf_protected(view):
    """Valida CSRF en formularios públicos que no requieren inicio de sesión."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if request.method in _MUTATING_METHODS:
            validate_csrf()
        return view(*args, **kwargs)

    return wrapped


def current_user() -> dict | None:
    if getattr(g, "_user_loaded", False):
        return g.current_user

    g._user_loaded = True
    user_id = session.get("user_id")
    if not isinstance(user_id, int):
        g.current_user = None
        return None

    try:
        g.current_user = find_user_by_id(user_id)
    except DatabaseConfigurationError:
        current_app.logger.exception("Falta configuración de la base de datos.")
        abort(503, description="La base de datos no está configurada. Revisa DATABASE_URL.")
    except psycopg.Error:
        current_app.logger.exception("No se pudo cargar la cuenta de la sesión.")
        abort(503, description="No se pudo conectar con PostgreSQL. Revisa la conexión.")

    if g.current_user is None:
        session.clear()
    return g.current_user


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if current_user() is None:
            return _login_redirect()
        if request.method in _MUTATING_METHODS:
            validate_csrf()
        return view(*args, **kwargs)

    return wrapped


def _login_redirect():
    target = request.full_path.rstrip("?")
    return redirect(url_for("auth.login", next=target))


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = current_user()
        if user is None:
            return _login_redirect()
        if user["rol"] != "admin":
            abort(403)
        if request.method in _MUTATING_METHODS:
            validate_csrf()
        return view(*args, **kwargs)

    return wrapped
