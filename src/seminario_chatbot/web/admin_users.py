"""Rutas administrativas para crear, consultar, editar y eliminar cuentas."""

from functools import wraps

import psycopg
from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.security import generate_password_hash

from seminario_chatbot.database import DatabaseConfigurationError
from seminario_chatbot.repositories.users import (
    EmailAlreadyExists,
    LastAdminProtected,
    SelfAccountDeleteBlocked,
    SelfAdminRoleChangeBlocked,
    UserNotFound,
    create_user,
    delete_user,
    find_user_for_admin,
    list_users,
    update_user,
)
from seminario_chatbot.validation import is_valid_email, normalize_email
from seminario_chatbot.web.security import admin_required


admin_users_bp = Blueprint("admin_users", __name__, url_prefix="/admin/usuarios")
_ALLOWED_ROLES = {"usuario", "admin"}


def _database_errors(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        try:
            return view(*args, **kwargs)
        except DatabaseConfigurationError:
            current_app.logger.exception("Falta configuración de la base de datos.")
            abort(503, description="La base de datos no está configurada. Revisa DATABASE_URL.")
        except psycopg.Error:
            current_app.logger.exception("Falló una operación administrativa de usuarios.")
            abort(503, description="No se pudo completar la operación. Revisa la conexión a PostgreSQL.")

    return wrapped


def _validate_fields(values: dict[str, str], password: str, password_required: bool) -> dict[str, str]:
    errors: dict[str, str] = {}
    if not values["nombre"]:
        errors["nombre"] = "El nombre es obligatorio."
    elif len(values["nombre"]) > 120:
        errors["nombre"] = "El nombre debe tener como máximo 120 caracteres."

    if not values["correo"] or not is_valid_email(values["correo"]):
        errors["correo"] = "Escribe un correo válido de hasta 254 caracteres."

    if values["rol"] not in _ALLOWED_ROLES:
        errors["rol"] = "Selecciona un rol válido."

    if password_required and len(password) < 10:
        errors["password"] = "La contraseña debe tener al menos 10 caracteres."
    elif password and len(password) < 10:
        errors["password"] = "La contraseña debe tener al menos 10 caracteres."
    return errors


def _render_form(
    mode: str,
    values: dict[str, str],
    errors: dict[str, str] | None = None,
    user_id: int | None = None,
    status: int = 200,
):
    return (
        render_template(
            "admin_user_form.html",
            mode=mode,
            values=values,
            errors=errors or {},
            user_id=user_id,
        ),
        status,
    )


@admin_users_bp.get("/")
@_database_errors
@admin_required
def index():
    return render_template("admin_users.html", users=list_users(), current_user=g.current_user)


@admin_users_bp.route("/nuevo", methods=["GET", "POST"])
@_database_errors
@admin_required
def create():
    if request.method == "GET":
        return _render_form(
            "crear",
            {"nombre": "", "correo": "", "rol": "usuario"},
        )

    values = {
        "nombre": request.form.get("nombre", "").strip(),
        "correo": normalize_email(request.form.get("correo", "")),
        "rol": request.form.get("rol", "usuario").strip(),
    }
    password = request.form.get("password", "")
    errors = _validate_fields(values, password, password_required=True)
    if errors:
        return _render_form("crear", values, errors, status=400)

    try:
        create_user(
            values["nombre"],
            values["correo"],
            generate_password_hash(password),
            values["rol"],
        )
    except EmailAlreadyExists:
        errors["correo"] = "Ya existe una cuenta con ese correo."
        return _render_form("crear", values, errors, status=409)

    flash("La cuenta se creó correctamente.", "success")
    return redirect(url_for("admin_users.index"))


@admin_users_bp.route("/<int:user_id>/editar", methods=["GET", "POST"])
@_database_errors
@admin_required
def edit(user_id: int):
    user = find_user_for_admin(user_id)
    if user is None:
        flash("La cuenta solicitada ya no existe.", "error")
        return redirect(url_for("admin_users.index"))

    if request.method == "GET":
        values = {"nombre": user["nombre"], "correo": user["correo"], "rol": user["rol"]}
        return _render_form("editar", values, user_id=user_id)

    values = {
        "nombre": request.form.get("nombre", "").strip(),
        "correo": normalize_email(request.form.get("correo", "")),
        "rol": request.form.get("rol", "").strip(),
    }
    password = request.form.get("password", "")
    errors = _validate_fields(values, password, password_required=False)
    actor_id = g.current_user["id_usuario"]
    if user_id == actor_id and values["rol"] != "admin":
        errors["rol"] = "No puedes quitarte tu propio rol de administrador."
    if errors:
        return _render_form("editar", values, errors, user_id=user_id, status=400)

    password_hash = generate_password_hash(password) if password else None
    try:
        update_user(
            user_id,
            actor_id,
            values["nombre"],
            values["correo"],
            values["rol"],
            password_hash,
        )
    except EmailAlreadyExists:
        errors["correo"] = "Ya existe una cuenta con ese correo."
        return _render_form("editar", values, errors, user_id=user_id, status=409)
    except UserNotFound:
        flash("La cuenta solicitada ya no existe.", "error")
        return redirect(url_for("admin_users.index"))
    except LastAdminProtected:
        errors["rol"] = "Debe quedar al menos una cuenta con rol administrador."
        return _render_form("editar", values, errors, user_id=user_id, status=409)
    except SelfAdminRoleChangeBlocked:
        errors["rol"] = "No puedes quitarte tu propio rol de administrador."
        return _render_form("editar", values, errors, user_id=user_id, status=400)

    flash("La cuenta se actualizó correctamente.", "success")
    return redirect(url_for("admin_users.index"))


@admin_users_bp.post("/<int:user_id>/eliminar")
@_database_errors
@admin_required
def remove(user_id: int):
    try:
        delete_user(user_id, g.current_user["id_usuario"])
    except SelfAccountDeleteBlocked:
        flash("No puedes eliminar la cuenta con la que tienes la sesión abierta.", "error")
    except LastAdminProtected:
        flash("Debe quedar al menos una cuenta con rol administrador.", "error")
    except UserNotFound:
        flash("La cuenta solicitada ya no existe.", "error")
    else:
        flash("La cuenta y sus datos asociados se eliminaron.", "success")
    return redirect(url_for("admin_users.index"))
