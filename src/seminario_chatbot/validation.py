"""Validaciones sencillas compartidas por las interfaces de la aplicación."""

import re


_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+$")


def normalize_email(email: str) -> str:
    return email.strip().casefold()


def is_valid_email(email: str) -> bool:
    return len(email) <= 254 and bool(_EMAIL_PATTERN.fullmatch(email))
