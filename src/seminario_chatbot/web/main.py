"""Páginas privadas principales."""

from flask import Blueprint, g, render_template

from seminario_chatbot.web.security import admin_required, login_required


main_bp = Blueprint("main", __name__)


@main_bp.get("/")
@login_required
def dashboard():
    return render_template("dashboard.html", user=g.current_user)


@main_bp.get("/admin")
@admin_required
def admin_panel():
    return render_template("admin.html", user=g.current_user)
