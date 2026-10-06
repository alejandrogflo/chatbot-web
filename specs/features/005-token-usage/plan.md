# Plan — F-005 Registro y gráfica de consumo

**Estado:** Completo

## Diseño

1. Añadir `database/002_nullable_consumption_category.sql`, una migración aditiva que relaja `NOT NULL` en `public.consumo_tokens.categoria`. Mantener el `CHECK` que limita las categorías no nulas a `peliculas` y `videojuegos`.
2. Ampliar `save_exchange` para recibir categoría, palabras académicas y tokens del proveedor; insertar conversación, mensajes y un registro de consumo dentro de una sola conexión/transacción.
3. Pasar al repositorio los valores `categoria`, `tokens_palabras` y `tokens_proveedor` ya producidos por `run_chat`; validar categoría y normalizar conteos no negativos antes de persistir.
4. Crear `repositories/consumption.py` para agregar por categoría con filtros SQL parametrizados por `id_usuario`, incluyendo un grupo de categoría nula.
5. Crear una ruta autenticada `/consumo` que consulta solo el id de `g.current_user`, prepara las series de películas, videojuegos y sin categoría y calcula el ancho relativo de las barras.
6. Crear una plantilla de consumo con la gráfica HTML accesible, totales y explicación del conteo. Enlazarla desde la navegación compartida y la tarjeta de inicio.
7. Actualizar decisiones de arquitectura, tareas y roadmap. Revisar el diff y los criterios sin ejecutar pruebas, como dispone `AGENTS.md`.

## Límites técnicos

- Sin nuevas dependencias: usar consultas SQL parametrizadas, Jinja y CSS existente.
- Cada lectura y escritura usa `DATABASE_URL` existente.
- El repositorio agrega usando `GROUP BY categoria`; el backend completa categorías con cero para que ambas barras siempre se representen.
- Los errores de conexión siguen el manejo de error 503 usado por el historial y no revelan detalles internos.
- La migración no se aplica automáticamente al iniciar la app y no toca las tablas de catálogo.
