"""Rutas para iniciar y cerrar sesión."""

from urllib.parse import urlsplit, urlunsplit

import psycopg
from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from seminario_chatbot.database import DatabaseConfigurationError
from seminario_chatbot.repositories.users import find_user_by_email
from seminario_chatbot.validation import normalize_email
from seminario_chatbot.web.security import csrf_protected, current_user, login_required


auth_bp = Blueprint("auth", __name__)


def _safe_next(value: str | None) -> str:
    if not value or "\\" in value:
        return url_for("main.dashboard")
    parsed = urlsplit(value)
    if (
        not value.startswith("/")
        or value.startswith("//")
        or value.startswith("/\\")
        or parsed.scheme
        or parsed.netloc
    ):
        return url_for("main.dashboard")
    return urlunsplit(("", "", parsed.path, parsed.query, ""))


@auth_bp.route("/login", methods=["GET", "POST"])
@csrf_protected
def login():
    if current_user() is not None:
        return redirect(url_for("main.dashboard"))

    next_target = request.form.get("next") if request.method == "POST" else request.args.get("next")
    if request.method == "POST":
        email = normalize_email(request.form.get("email", ""))
        password = request.form.get("password", "")
        try:
            user = find_user_by_email(email) if email and password else None
        except DatabaseConfigurationError:
            current_app.logger.exception("Falta configuración de la base de datos.")
            flash("La base de datos no está configurada. Revisa DATABASE_URL.", "error")
        except psycopg.Error:
            current_app.logger.exception("No se pudo validar el inicio de sesión.")
            flash("No se pudo conectar con PostgreSQL. Revisa la conexión.", "error")
        else:
            if user and check_password_hash(user["password_hash"], password):
                session.clear()
                session["user_id"] = user["id_usuario"]
                return redirect(_safe_next(next_target))
            flash("El correo o la contraseña no son válidos.", "error")

    return render_template("login.html", next_target=next_target or "")


@auth_bp.post("/logout")
@login_required
def logout():
    session.clear()
    flash("Has cerrado sesión.", "success")
    return redirect(url_for("auth.login"))
