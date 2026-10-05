# Especificación del producto

**Estado:** Lista como definición inicial del alcance  
**Fuente principal:** [pf.md](../pf.md), el enunciado del proyecto final

## Propósito

Construir una aplicación web en español para consultar un catálogo existente de películas y videojuegos mediante un chatbot con IA. El sistema debe integrar interfaz, backend, PostgreSQL y un proveedor de IA, con acceso diferenciado para administradores y usuarios.

## Usuarios y necesidades

- **Usuario:** iniciar y cerrar sesión, consultar el catálogo en lenguaje natural, revisar sus preguntas y respuestas anteriores y ver su consumo aproximado separado por categoría.
- **Administrador:** gestionar las cuentas y mantener los catálogos de películas y videojuegos.
- **Visitante sin sesión:** no puede acceder a datos ni a funciones internas de la aplicación.

No existe registro público: el administrador crea las cuentas.

## Alcance funcional

### FR-01 — Cuentas y acceso

El sistema permite iniciar y cerrar sesión. Cada cuenta tiene un rol de usuario o administrador. El administrador puede crear, consultar, actualizar y eliminar cuentas. El acceso a operaciones protegidas se autoriza en el servidor según la cuenta y su rol.

### FR-02 — Administración de catálogos

El administrador puede crear, consultar, actualizar y eliminar registros de películas y videojuegos. Los usuarios normales no pueden modificar los catálogos.

### FR-03 — Chat sobre catálogos

Un usuario autenticado puede preguntar por películas o videojuegos presentes en la base de datos. El sistema identifica la categoría y los filtros solicitados, consulta la información pertinente y redacta una respuesta en español respaldada por esos resultados. Si la categoría no se puede identificar, solicita una aclaración. Si no hay resultados, lo comunica sin inventar registros.

Cada pregunta se procesa independientemente: no se requiere memoria conversacional.

### FR-04 — Historial privado

El sistema guarda las preguntas y respuestas. Un usuario puede consultar solo su propio historial, presentado como mínimo con fecha, pregunta y respuesta.

### FR-05 — Consumo aproximado

Para la evaluación del curso, una palabra procesada se considera un token. El sistema registra el consumo de cada consulta y permite al usuario ver una gráfica de barras que diferencia películas de videojuegos. La interfaz explica que se trata de una aproximación académica.

### FR-06 — Experiencia y errores

La interfaz debe ser clara, usable y estar en español. Los errores de configuración o de servicio se presentan con mensajes comprensibles, sin exponer secretos ni detalles internos. La ausencia de una clave de IA no debe simular respuestas del modelo.

## Criterios de aceptación del producto

- Una persona sin sesión no puede usar el chat, consultar historiales ni acceder a operaciones administrativas.
- Un usuario puede iniciar sesión con su cuenta y finalizar su sesión explícitamente.
- Un administrador puede gestionar cuentas y ambos catálogos; un usuario normal no puede ejecutar esas operaciones aunque intente acceder directamente a sus rutas.
- Una pregunta sobre una categoría devuelve datos de ese catálogo, y cada título afirmado en la respuesta se respalda en resultados recuperados.
- Una pregunta ambigua solicita la categoría. Una consulta sin coincidencias indica que no encontró resultados.
- Una pregunta y su respuesta aparecen en el historial de la cuenta que hizo la consulta y no en el de otras cuentas.
- La gráfica muestra el consumo propio agregado por películas y videojuegos y describe la regla de conteo por palabras.
- Si falta la configuración de IA, la aplicación explica cómo configurarla al intentar usar esa capacidad; no fabrica una respuesta de IA.
- Las tablas de catálogo proporcionadas por el curso conservan sus datos durante la instalación y evolución del sistema.

## Fuera de alcance

- Memoria entre preguntas o conversación contextual persistente.
- Registro de cuentas por el público.
- Ejecución de SQL generado o escrito por el modelo.
- CRUD administrativo para conversaciones, mensajes o registros de consumo; estas tablas se mantienen automáticamente.
- Sustitución, limpieza o recarga de las tablas de películas y videojuegos existentes.

## Supuestos y decisiones registradas

- El esquema y los datos iniciales de `public.peliculas` y `public.videojuegos` ya fueron proporcionados y deben preservarse.
- Las contraseñas se almacenan mediante hashes seguros; nunca en texto plano.
- La palabra es la unidad académica para el consumo visible. Cuando el proveedor entregue consumo real, puede guardarse por separado para comparación.
- Las reglas técnicas concretas se documentan en [01-architecture.md](01-architecture.md), no en esta especificación de comportamiento.

