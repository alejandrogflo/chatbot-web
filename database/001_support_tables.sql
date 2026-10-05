-- Migración aditiva para el proyecto final.
-- No modifica ni vuelve a cargar public.peliculas o public.videojuegos.
BEGIN;

CREATE TABLE IF NOT EXISTS public.usuarios (
    id_usuario BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    correo VARCHAR(254) NOT NULL,
    password_hash TEXT NOT NULL,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('usuario', 'admin')),
    fecha_registro TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS usuarios_correo_lower_uq
    ON public.usuarios (LOWER(correo));

CREATE TABLE IF NOT EXISTS public.conversaciones (
    id_conversacion BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_usuario BIGINT NOT NULL
        REFERENCES public.usuarios (id_usuario) ON DELETE CASCADE,
    fecha_creacion TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS conversaciones_usuario_fecha_idx
    ON public.conversaciones (id_usuario, fecha_creacion DESC);

CREATE TABLE IF NOT EXISTS public.mensajes (
    id_mensaje BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_conversacion BIGINT NOT NULL
        REFERENCES public.conversaciones (id_conversacion) ON DELETE CASCADE,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('usuario', 'asistente')),
    contenido TEXT NOT NULL,
    fecha TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS mensajes_conversacion_fecha_idx
    ON public.mensajes (id_conversacion, fecha);

CREATE TABLE IF NOT EXISTS public.consumo_tokens (
    id_consumo BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_usuario BIGINT NOT NULL
        REFERENCES public.usuarios (id_usuario) ON DELETE CASCADE,
    id_conversacion BIGINT NOT NULL
        REFERENCES public.conversaciones (id_conversacion) ON DELETE CASCADE,
    categoria VARCHAR(20) NOT NULL CHECK (categoria IN ('peliculas', 'videojuegos')),
    tokens INTEGER NOT NULL CHECK (tokens >= 0),
    tokens_proveedor INTEGER CHECK (tokens_proveedor IS NULL OR tokens_proveedor >= 0),
    fecha TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS consumo_usuario_categoria_fecha_idx
    ON public.consumo_tokens (id_usuario, categoria, fecha DESC);

COMMIT;
