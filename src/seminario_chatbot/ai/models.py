from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Category = Literal["peliculas", "videojuegos"]


class QueryPlan(BaseModel):
    """Filtros permitidos que el LLM extrae de una pregunta en lenguaje natural."""

    model_config = ConfigDict(extra="forbid")

    categoria: Category | None = Field(
        default=None,
        description="peliculas, videojuegos, o null si la pregunta no permite decidir.",
    )
    genero: str | None = Field(
        default=None,
        max_length=80,
        description=(
            "Género pedido. Conserva la forma del catálogo cuando sea conocida; "
            "normaliza 'disparos' o 'tiros' a 'Shooter'."
        ),
    )
    plataforma: str | None = Field(default=None, max_length=100)
    titulo: str | None = Field(default=None, max_length=160)
    calificacion_minima: float | None = Field(default=None, ge=0, le=10)
    calificacion_minima_inclusiva: bool = Field(
        default=True,
        description="True para 'al menos'; False para 'mayor que'.",
    )
    calificacion_maxima: float | None = Field(default=None, ge=0, le=10)
    calificacion_maxima_inclusiva: bool = Field(
        default=True,
        description="True para 'como máximo'; False para 'menor que'.",
    )
    anio_desde: int | None = Field(default=None, ge=1888, le=2200)
    anio_hasta: int | None = Field(default=None, ge=1888, le=2200)
    limite: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Cantidad máxima solicitada; usa 5 si no se especifica.",
    )
