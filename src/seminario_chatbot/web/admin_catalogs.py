"""Rutas administrativas para mantener los catálogos existentes."""

from decimal import Decimal, InvalidOperation
from functools import wraps

import psycopg
from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, request, url_for

from seminario_chatbot.database import DatabaseConfigurationError
from seminario_chatbot.repositories.catalogs import (
    CatalogItemNotFound,
    create_catalog_item,
    delete_catalog_item,
    find_catalog_item,
    get_catalog_definition,
    list_catalog_items,
    update_catalog_item,
)
from seminario_chatbot.web.security import admin_required


admin_catalogs_bp = Blueprint("admin_catalogs", __name__, url_prefix="/admin/catalogos")


def _database_errors(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        try:
            return view(*args, **kwargs)
        except DatabaseConfigurationError:
            current_app.logger.exception("Falta configuración de la base de datos.")
            abort(503, description="La base de datos no está configurada. Revisa DATABASE_URL.")
        except psycopg.Error:
            current_app.logger.exception("Falló una operación administrativa de catálogo.")
            abort(503, description="No se pudo completar la operación. Revisa la conexión a PostgreSQL.")

    return wrapped


def _catalog_or_404(catalog_key: str) -> dict:
    definition = get_catalog_definition(catalog_key)
    if definition is None:
        abort(404)
    return definition


def _parse_values(definition: dict) -> tuple[dict, dict]:
    values = {}
    errors = {}
    for field in definition["fields"]:
        name = field["name"]
        raw_value = request.form.get(name, "").strip()
        label = field["label"]

        if not raw_value:
            if field.get("required"):
                errors[name] = f"{label} es obligatorio."
            values[name] = None
            continue

        if field["kind"] in {"text", "textarea"}:
            max_length = field.get("max_length")
            if max_length and len(raw_value) > max_length:
                errors[name] = f"{label} debe tener como máximo {max_length} caracteres."
            values[name] = raw_value
            continue

        if field["kind"] == "integer":
            try:
                number = int(raw_value, 10)
            except ValueError:
                errors[name] = f"{label} debe ser un número entero."
                values[name] = None
                continue
            if field.get("min") is not None and number < field["min"]:
                errors[name] = f"{label} no puede ser menor que {field['min']}."
            elif field.get("max") is not None and number > field["max"]:
                errors[name] = f"{label} no puede superar {field['max']}."
            values[name] = number
            continue

        if field["kind"] == "decimal":
            try:
                number = Decimal(raw_value)
            except InvalidOperation:
                errors[name] = f"{label} debe ser un número válido."
                values[name] = None
                continue
            if not number.is_finite():
                errors[name] = f"{label} debe ser un número válido."
            elif number < field["min"] or number > field["max"]:
                errors[name] = f"{label} debe estar entre {field['min']} y {field['max']}."
            elif number.as_tuple().exponent < -1:
                errors[name] = f"{label} puede tener como máximo una cifra decimal."
            values[name] = number

    return values, errors


def _render_form(
    catalog_key: str,
    definition: dict,
    values: dict,
    errors: dict | None = None,
    item_id: int | None = None,
    status: int = 200,
):
    return (
        render_template(
            "admin_catalog_item_form.html",
            catalog_key=catalog_key,
            catalog=definition,
            values=values,
            errors=errors or {},
            item_id=item_id,
        ),
        status,
    )


@admin_catalogs_bp.get("/<catalog_key>/")
@_database_errors
@admin_required
def index(catalog_key: str):
    definition = _catalog_or_404(catalog_key)
    return render_template(
        "admin_catalog_items.html",
        catalog_key=catalog_key,
        catalog=definition,
        field_labels={field["name"]: field["label"] for field in definition["fields"]},
        items=list_catalog_items(catalog_key),
        current_user=g.current_user,
    )


@admin_catalogs_bp.route("/<catalog_key>/nuevo", methods=["GET", "POST"])
@_database_errors
@admin_required
def create(catalog_key: str):
    definition = _catalog_or_404(catalog_key)
    if request.method == "GET":
        values = {field["name"]: "" for field in definition["fields"]}
        return _render_form(catalog_key, definition, values)

    values, errors = _parse_values(definition)
    if errors:
        return _render_form(catalog_key, definition, values, errors, status=400)

    create_catalog_item(catalog_key, values)
    flash("El registro se creó correctamente.", "success")
    return redirect(url_for("admin_catalogs.index", catalog_key=catalog_key))


@admin_catalogs_bp.route("/<catalog_key>/<int:item_id>/editar", methods=["GET", "POST"])
@_database_errors
@admin_required
def edit(catalog_key: str, item_id: int):
    definition = _catalog_or_404(catalog_key)
    item = find_catalog_item(catalog_key, item_id)
    if item is None:
        flash("El registro solicitado ya no existe.", "error")
        return redirect(url_for("admin_catalogs.index", catalog_key=catalog_key))

    if request.method == "GET":
        values = {field["name"]: item[field["name"]] for field in definition["fields"]}
        return _render_form(catalog_key, definition, values, item_id=item_id)

    values, errors = _parse_values(definition)
    if errors:
        return _render_form(catalog_key, definition, values, errors, item_id=item_id, status=400)

    try:
        update_catalog_item(catalog_key, item_id, values)
    except CatalogItemNotFound:
        flash("El registro solicitado ya no existe.", "error")
        return redirect(url_for("admin_catalogs.index", catalog_key=catalog_key))

    flash("El registro se actualizó correctamente.", "success")
    return redirect(url_for("admin_catalogs.index", catalog_key=catalog_key))


@admin_catalogs_bp.post("/<catalog_key>/<int:item_id>/eliminar")
@_database_errors
@admin_required
def remove(catalog_key: str, item_id: int):
    _catalog_or_404(catalog_key)
    try:
        delete_catalog_item(catalog_key, item_id)
    except CatalogItemNotFound:
        flash("El registro solicitado ya no existe.", "error")
    else:
        flash("El registro se eliminó correctamente.", "success")
    return redirect(url_for("admin_catalogs.index", catalog_key=catalog_key))
