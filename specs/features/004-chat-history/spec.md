# F-004 — Chat web e historial privado

**Estado:** Completa; revisión estática el 2026-10-05, sin ejecución de pruebas según las instrucciones del repositorio
**Prioridad:** Necesaria para consultar los catálogos desde la aplicación y revisar respuestas anteriores
**Depende de:** F-001 (autenticación), M2 (grafo LangGraph) y las tablas de soporte existentes

## Problema

El grafo de consulta ya puede responder desde la CLI, pero la aplicación web aún no ofrece un chat. Tampoco guarda las preguntas y respuestas que exige el historial por usuario.

## Resultado esperado

Una persona autenticada puede enviar una pregunta independiente sobre películas o videojuegos, recibir la salida del grafo existente y abrir un historial privado con fecha, pregunta y respuesta. La web no usa contexto de preguntas anteriores.

## Alcance y comportamiento

- El panel del usuario ofrece accesos al chat y al historial.
- El formulario acepta una pregunta no vacía de hasta 2,000 caracteres; la validación se aplica en el servidor y se refleja también en la interfaz.
- Cada envío válido invoca `run_chat` del grafo LangGraph con una pregunta nueva. No se agrega memoria ni un checkpointer.
- Cada envío crea una fila en `conversaciones` y, dentro de la misma transacción, un mensaje `usuario` y uno `asistente` en `mensajes`.
- La respuesta persistida es la respuesta del grafo, incluidas las respuestas de respaldo y los mensajes comprensibles de error de configuración/servicio que el grafo devuelve.
- El detalle de una consulta contiene solo esa pregunta y su respuesta. El historial se presenta en una tabla con fecha, pregunta, respuesta y acceso al detalle.
- Todas las lecturas del historial se filtran por el identificador de la sesión en el repositorio. Intentar abrir la conversación de otra cuenta no revela su contenido.
- El chat y el historial requieren sesión; las mutaciones usan la protección CSRF existente.
- Los errores de PostgreSQL o fallos inesperados se registran en el servidor y se muestran con un mensaje en español sin detalles internos.
- F-004 no registra consumo ni dibuja la gráfica; eso corresponde a F-005. No modifica el esquema ni los catálogos.

## Criterios de aceptación

### AC-1 — Acceso autenticado

Una visita anónima al chat, al historial o al detalle se redirige al login. El envío de pregunta no se procesa sin una sesión válida y token CSRF válido.

### AC-2 — Chat integrado

Un usuario autenticado puede enviar una pregunta válida. La aplicación invoca el grafo LangGraph existente y presenta su respuesta, incluida una aclaración cuando la categoría es ambigua y mensajes de configuración claros cuando falta el proveedor.

### AC-3 — Persistencia atómica

Cada pregunta procesada crea una conversación propiedad del usuario y guarda sus mensajes de usuario y asistente. Si falla la persistencia, la solicitud no afirma que el intercambio quedó guardado.

### AC-4 — Historial privado

El usuario ve sus consultas con fecha, pregunta y respuesta. No aparecen consultas de otras cuentas; abrir un identificador ajeno se trata como inexistente.

### AC-5 — Preguntas independientes

Una consulta nueva inicia un estado nuevo del grafo y no recibe mensajes de conversaciones anteriores. El detalle de cada conversación muestra solo su pregunta y respuesta.

### AC-6 — Validación y mensajes

Una pregunta vacía o de más de 2,000 caracteres se rechaza sin invocar el grafo ni guardar conversación. Los fallos de base de datos o inesperados no exponen trazas, secretos ni consultas SQL.

### AC-7 — Sin cambios ajenos

No se agregan migraciones ni se modifican, borran o recargan filas de `peliculas` o `videojuegos`. No se implementa el registro de consumo de F-005.

## Fuera de alcance

- Memoria de varios turnos, conversación contextual o edición/eliminación de historial.
- Registro de consumo de tokens y gráfica por categoría (F-005).
- Cambio del grafo, prompts, esquema PostgreSQL o CRUD de catálogos.
- Historial administrativo de todos los usuarios.

## Supuestos

- `public.conversaciones` y `public.mensajes` ya existen según `database/001_support_tables.sql` y están aplicadas localmente.
- El grafo devuelve una respuesta utilizable para aclaraciones y errores conocidos; esos intercambios también forman parte del historial solicitado.
- Las fechas se presentan usando el timestamp guardado por PostgreSQL, sin introducir una conversión de zona horaria en este incremento.
