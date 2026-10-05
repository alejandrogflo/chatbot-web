"""Aplicación web Flask."""

import os

from flask import Flask, request

from seminario_chatbot.settings import get_settings


def _env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().casefold() in {"1", "true", "yes", "on"}


def create_app() -> Flask:
    """Construye la aplicación y valida la configuración de sesión requerida."""
    settings = get_settings()
    if not settings.secret_key or len(settings.secret_key) < 32:
        raise RuntimeError(
            "SECRET_KEY falta o es demasiado corta. Define en .env un secreto aleatorio "
            "de al menos 32 caracteres "
            "antes de iniciar la aplicación web."
        )

    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=settings.secret_key,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=_env_flag("SESSION_COOKIE_SECURE"),
    )

    from seminario_chatbot.web.auth import auth_bp
    from seminario_chatbot.web.main import main_bp
    from seminario_chatbot.web.security import csrf_token, validate_csrf

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.context_processor(lambda: {"csrf_token": csrf_token})

    @app.before_request
    def protect_mutating_requests() -> None:
        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            validate_csrf()

    @app.errorhandler(400)
    def bad_request(error):
        return _render_error(400, "La solicitud no es válida.")

    @app.errorhandler(403)
    def forbidden(error):
        return _render_error(403, "No tienes permiso para abrir esta página.")

    @app.errorhandler(503)
    def unavailable(error):
        description = getattr(error, "description", "El servicio no está disponible.")
        return _render_error(503, description)

    return app


def _render_error(status: int, message: str):
    from flask import render_template

    return render_template("error.html", status=status, message=message), status
