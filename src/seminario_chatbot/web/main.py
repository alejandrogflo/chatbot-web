"""Páginas privadas principales."""

import logging

import psycopg
from flask import Blueprint, abort, g, redirect, render_template, request, url_for

from seminario_chatbot.database import DatabaseConfigurationError
from seminario_chatbot.repositories.conversations import (
    find_user_conversation,
    list_user_conversations,
)
from seminario_chatbot.services.chat import ChatProcessingError, process_question
from seminario_chatbot.web.security import admin_required, login_required


main_bp = Blueprint("main", __name__)
logger = logging.getLogger(__name__)


@main_bp.get("/")
@login_required
def dashboard():
    return render_template("dashboard.html", user=g.current_user)


@main_bp.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    if request.method == "GET":
        return render_template("chat.html", user=g.current_user, question="")

    submitted_question = request.form.get("question", "")
    if len(submitted_question) > 2000:
        return (
            render_template(
                "chat.html",
                user=g.current_user,
                question="",
                form_error="La pregunta no puede superar 2,000 caracteres.",
            ),
            400,
        )

    question = submitted_question.strip()
    if not question:
        return (
            render_template(
                "chat.html",
                user=g.current_user,
                question=question,
                form_error="Escribe una pregunta antes de enviarla.",
            ),
            400,
        )
    try:
        result = process_question(g.current_user["id_usuario"], question)
    except DatabaseConfigurationError:
        logger.exception("No está configurada la base de datos para guardar el chat.")
        abort(
            503,
            description="No se pudo guardar la consulta. Revisa la configuración de PostgreSQL.",
        )
    except psycopg.Error:
        logger.exception("No se pudo guardar la conversación en PostgreSQL.")
        abort(
            503,
            description="No se pudo guardar la consulta. Revisa la conexión con PostgreSQL.",
        )
    except ChatProcessingError:
        logger.exception("El grafo no produjo una respuesta para la consulta web.")
        return (
            render_template(
                "chat.html",
                user=g.current_user,
                question=question,
                form_error="No se pudo completar la consulta. Inténtalo de nuevo.",
            ),
            502,
        )
    except Exception:
        logger.exception("Falló el procesamiento web de una consulta.")
        return (
            render_template(
                "chat.html",
                user=g.current_user,
                question=question,
                form_error="No se pudo completar la consulta. Inténtalo de nuevo.",
            ),
            502,
        )

    return redirect(
        url_for("main.conversation_detail", conversation_id=result["id_conversacion"]),
        code=303,
    )


@main_bp.get("/historial")
@login_required
def history():
    try:
        conversations = list_user_conversations(g.current_user["id_usuario"])
    except DatabaseConfigurationError:
        logger.exception("No está configurada la base de datos para leer el historial.")
        abort(
            503,
            description="No se pudo cargar el historial. Revisa la configuración de PostgreSQL.",
        )
    except psycopg.Error:
        logger.exception("No se pudo leer el historial desde PostgreSQL.")
        abort(
            503,
            description="No se pudo cargar el historial. Revisa la conexión con PostgreSQL.",
        )

    return render_template(
        "history.html",
        user=g.current_user,
        conversations=conversations,
    )


@main_bp.get("/historial/<int:conversation_id>")
@login_required
def conversation_detail(conversation_id: int):
    try:
        conversation = find_user_conversation(
            g.current_user["id_usuario"], conversation_id
        )
    except DatabaseConfigurationError:
        logger.exception("No está configurada la base de datos para leer una conversación.")
        abort(
            503,
            description="No se pudo abrir la consulta. Revisa la configuración de PostgreSQL.",
        )
    except psycopg.Error:
        logger.exception("No se pudo leer una conversación desde PostgreSQL.")
        abort(
            503,
            description="No se pudo abrir la consulta. Revisa la conexión con PostgreSQL.",
        )

    if conversation is None:
        abort(404)
    return render_template(
        "conversation.html",
        user=g.current_user,
        conversation=conversation,
    )


@main_bp.get("/admin")
@admin_required
def admin_panel():
    return render_template("admin.html", user=g.current_user)
