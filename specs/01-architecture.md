# Arquitectura y decisiones técnicas

**Estado:** Base técnica acordada; F-001 y F-002 implementados y revisados manualmente
**Actualizado:** 2026-10-05

## Tecnologías

- Python 3.11 o posterior.
- Flask para la aplicación web.
- PostgreSQL para persistencia.
- HTML, CSS y JavaScript sencillo para la interfaz.
- LangGraph para orquestar el flujo de consulta de IA.
- LangChain Groq / ChatGroq como integración con el proveedor, con modelo y secreto configurados por entorno.
- Psycopg para conectar Python con PostgreSQL.
- Pydantic para validar el plan estructurado de filtros.

DBeaver es una herramienta de inspección y administración manual. La aplicación se conecta directamente a PostgreSQL y no depende de DBeaver.

## Estado técnico comprobado en el repositorio

### Implementado

- Acceso de solo lectura a los catálogos mediante identificadores permitidos y valores SQL parametrizados en `src/seminario_chatbot/database.py`.
- Modelos Pydantic acotados para categoría y filtros de consulta.
- Grafo LangGraph con planificación, aclaración, consulta, redacción, evaluación determinista y manejo de errores.
- Respuesta de respaldo construida desde filas PostgreSQL cuando no se puede redactar o no se supera la comprobación de fundamentación.
- Configuración por variables de entorno, ejemplos de evaluación del planificador y CLI para explorar el grafo.
- Migración aditiva `database/001_support_tables.sql`, ya aplicada en el entorno local según `AGENTS.md`.
- Aplicación Flask inicial con login/logout, sesiones protegidas, autorización administrativa por solicitud, comando de primer administrador y formularios protegidos con CSRF.
- CRUD web inicial de usuarios: repositorio con consultas parametrizadas, formulario de alta/edición y listado sin hashes, eliminación protegida y límites para conservar acceso administrador.

### Pendiente

- CRUD web administrativo de películas y videojuegos.
- Persistencia web de preguntas, respuestas y consumo.
- Historial privado y agregación/gráfica de consumo.
- Instrucciones finales de ejecución y guion de demostración.

## Componentes propuestos

1. **Interfaz Flask:** páginas y formularios en español; muestra solo las acciones permitidas al rol, sin usar la interfaz como único control de acceso.
2. **Capa de aplicación:** coordina autenticación, administración, chat, historial y consumo. Las rutas delegan en esta capa y no contienen SQL ni lógica del modelo.
3. **Repositorios PostgreSQL:** consultas parametrizadas para usuarios, catálogos, conversaciones, mensajes y consumo.
4. **Servicio de chat:** invoca el grafo LangGraph existente con una pregunta nueva por solicitud y persiste la interacción y su consumo.
5. **Grafo de IA:** convierte lenguaje natural en un plan validado, consulta solo los campos permitidos, redacta usando resultados recuperados y comprueba la fundamentación.

La estructura concreta de módulos puede ajustarse al implementar, conservando esos límites. No añadir capas o dependencias sin una necesidad clara del alcance.

### Organización del paquete

La capa web vive dentro de `src/seminario_chatbot/`: `web/` contiene la fábrica Flask, blueprints, templates y estáticos; `repositories/` contiene acceso PostgreSQL por dominio. Añadir servicios cuando una coordinación de casos de uso los requiera, sin carpetas vacías ni una capa genérica anticipada. Mantener `ai/`, `evaluation/` y la CLI como componentes separados.

## Flujo de chat

```text
Solicitud autenticada
  -> validar pregunta
  -> LangGraph extrae y valida categoría/filtros
  -> backend construye consulta parametrizada
  -> PostgreSQL devuelve filas limitadas
  -> modelo redacta a partir de esas filas
  -> evaluador determinista comprueba títulos
  -> respaldo desde datos si hace falta
  -> guardar pregunta, respuesta y consumo
  -> devolver respuesta e historial
```

Cada pregunta empieza con estado nuevo y el grafo no usa checkpointer. La aplicación no entrega SQL al modelo ni acepta SQL libre del usuario.

## Persistencia existente

Los catálogos viven en `public.peliculas` y `public.videojuegos`. Sus nombres, columnas y registros no se recrean ni se recargan. Consultar el esquema real antes de asumir columnas nuevas.

La migración existente añade:

- `usuarios`, con correo único sin distinguir mayúsculas/minúsculas y campo `password_hash`.
- `conversaciones`, vinculadas a usuarios.
- `mensajes`, con roles usuario/asistente.
- `consumo_tokens`, vinculado a usuario y conversación, con categoría y conteos académico y del proveedor.

La migración `001` ya se aplicó localmente; los cambios futuros requieren una nueva migración numerada. Para mantener aislado el historial y vincular cada costo a una consulta independiente, la aplicación debe crear una conversación por pregunta, con el mensaje del usuario, el del asistente y el consumo asociado.

## Límites de seguridad

- Credenciales y clave Groq solo desde entorno local; `.env` no se versiona.
- Contraseñas guardadas como hash seguro.
- Sesión requerida en servidor para operaciones privadas y autorización del rol en cada operación administrativa.
- Entradas validadas y consultas parametrizadas.
- Plan de IA restringido a categorías, campos, operadores y límites permitidos; el backend controla tabla y SQL.
- Filas y contexto enviados al modelo limitados a lo necesario.
- Historial y consumo filtrados por el usuario autenticado.
- Mensajes de error públicos claros, sin secretos ni trazas internas.
- Las reglas exactas de configuración y preservación del entorno están en [AGENTS.md](../AGENTS.md).

## Decisiones confirmadas durante F-001

- Templates y estáticos viven dentro de `src/seminario_chatbot/web/` para distribuirlos junto al paquete Python.
- El primer administrador se aprovisiona con `create-admin`, que solicita la contraseña de forma oculta y serializa el alta inicial con un bloqueo advisory de PostgreSQL.
- La web requiere `SECRET_KEY`; la cookie de sesión es HttpOnly y SameSite=Lax, y puede habilitar Secure mediante `SESSION_COOKIE_SECURE` cuando se use HTTPS.
- El usuario confirmó manualmente el 2026-10-05 los recorridos principales de inicio/cierre de sesión, acceso anónimo, autorización por rol y mensaje genérico de credenciales inválidas. Los detalles del entorno final de demostración siguen pendientes; las credenciales y URL locales no se copian a código.

## Decisiones confirmadas durante F-002

- El CRUD reutiliza `public.usuarios` y el índice único existente sobre `LOWER(correo)`; no añade migración.
- Las vistas administrativas solo consultan y presentan id, nombre, correo, rol y fecha; nunca leen el hash de contraseña para mostrarse.
- Al eliminar una cuenta se informa del borrado en cascada de conversaciones, mensajes y consumo. No se puede borrar la propia cuenta ni quitar la última cuenta administradora.
- El usuario confirmó manualmente el 2026-10-05 el acceso por rol, el listado sin hashes, alta y validaciones, edición con contraseña vacía, confirmación y eliminación de cuentas de prueba.
