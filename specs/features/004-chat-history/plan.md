# Plan — F-004 Chat web e historial privado

## Diseño

1. Añadir un repositorio de conversaciones que cree una conversación y ambos mensajes en una sola transacción, y que liste/lea conversaciones siempre condicionadas por `id_usuario`.
2. Añadir un servicio de chat pequeño que llame `run_chat(question)`, persista la pregunta y la respuesta devuelta y retorne el identificador y los metadatos necesarios para la vista. No reconstruir ni duplicar el grafo.
3. Extender el blueprint principal con `GET/POST /chat`, un detalle privado `/historial/<id>` y una lista `/historial`. El POST requiere login y reutiliza CSRF de `login_required`.
4. Validar y normalizar la entrada en el servidor: quitar espacios exteriores, rechazar vacío y limitar a 2,000 caracteres. Mostrar fallos previsibles en español sin detalles de PostgreSQL.
5. Reemplazar las tarjetas provisionales del dashboard con accesos funcionales y añadir templates para formulario de chat, respuesta y tabla/lista de historial, conservando el estilo existente y un diseño adaptable.
6. No guardar consumo todavía. La interfaz y el resultado del servicio mantendrán la información devuelta por el grafo disponible para la integración de F-005, sin escribir `consumo_tokens` en este incremento.
7. Registrar el estado final en arquitectura, roadmap y README después de completar el incremento.

## Límites técnicos

- No añadir dependencias, migraciones ni cambios al esquema existente.
- No cambiar el grafo ni pasar historial previo al modelo.
- La aplicación no forma SQL dinámico; usa sentencias parametrizadas para `usuarios`, `conversaciones` y `mensajes`.
- Los permisos se aplican en servidor y la propiedad se comprueba en cada lectura, no solo ocultando enlaces.
- No tocar datos ni estructura de `public.peliculas` o `public.videojuegos`.
- No ejecutar pruebas automatizadas; revisar cambios y criterios sin invocar suites, según las instrucciones del repositorio.

## Manejo de fallos

- Los errores controlados que el grafo devuelve como respuesta se presentan y se guardan como mensajes del asistente.
- Si falla PostgreSQL al leer o persistir, registrar el detalle solo en el log y devolver un mensaje público genérico con guía de configuración cuando corresponda.
- Si el grafo falla de forma inesperada, no fabricar ni persistir una respuesta; informar que no se completó la consulta.
