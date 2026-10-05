"""Comandos de consola para iniciar la web y crear el primer administrador."""

import getpass
import os
import sys

import psycopg
from werkzeug.security import generate_password_hash

from seminario_chatbot.database import DatabaseConfigurationError
from seminario_chatbot.repositories.users import (
    EmailAlreadyExists,
    InitialAdminAlreadyExists,
    create_initial_admin,
)
from seminario_chatbot.validation import is_valid_email, normalize_email


def run_web() -> int:
    from seminario_chatbot.web import create_app

    try:
        app = create_app()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    try:
        port = int(os.getenv("FLASK_PORT", "5000"))
    except ValueError:
        print("FLASK_PORT debe ser un número entero.", file=sys.stderr)
        return 2
    app.run(host=host, port=port)
    return 0


def create_admin() -> int:
    print("Crear primer administrador de Seminario Chatbot")
    try:
        name = input("Nombre: ").strip()
        email = normalize_email(input("Correo: "))
        password = getpass.getpass("Contraseña (mínimo 10 caracteres): ")
        confirmation = getpass.getpass("Confirma la contraseña: ")
    except (EOFError, KeyboardInterrupt):
        print("\nOperación cancelada.", file=sys.stderr)
        return 2

    errors = []
    if not name or len(name) > 120:
        errors.append("El nombre es obligatorio y debe tener como máximo 120 caracteres.")
    if not is_valid_email(email):
        errors.append("Escribe un correo válido de hasta 254 caracteres.")
    if len(password) < 10:
        errors.append("La contraseña debe tener al menos 10 caracteres.")
    if password != confirmation:
        errors.append("Las contraseñas no coinciden.")
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 2

    try:
        user_id = create_initial_admin(name, email, generate_password_hash(password))
    except InitialAdminAlreadyExists:
        print("Ya existe una cuenta administradora; no se creó otra.", file=sys.stderr)
        return 1
    except EmailAlreadyExists:
        print("Ese correo ya pertenece a una cuenta.", file=sys.stderr)
        return 1
    except DatabaseConfigurationError:
        print("DATABASE_URL no está configurada en el archivo .env.", file=sys.stderr)
        return 2
    except psycopg.Error:
        print("No se pudo guardar la cuenta. Revisa DATABASE_URL y PostgreSQL.", file=sys.stderr)
        return 1

    print(f"Administrador creado correctamente (id {user_id}).")
    return 0
