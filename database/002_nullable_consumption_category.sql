-- Permite registrar el consumo de una pregunta antes de identificar su categoría.
-- Las categorías conocidas siguen restringidas a peliculas y videojuegos.
BEGIN;

ALTER TABLE public.consumo_tokens
    ALTER COLUMN categoria DROP NOT NULL;

COMMIT;
