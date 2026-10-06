# F-003 — Administración de películas y videojuegos

**Estado:** En curso; diseño listo para implementar
**Prioridad:** Necesaria para que el administrador mantenga ambos catálogos
**Depende de:** F-001 (autenticación y autorización administrativa), ya completada

## Problema

Los catálogos existentes se pueden consultar desde el flujo de IA, pero todavía no hay pantallas para mantener sus registros desde la aplicación.

## Resultado esperado

Un administrador puede listar, crear, editar y eliminar registros individuales de películas y videojuegos. La aplicación opera sobre `public.peliculas` y `public.videojuegos` existentes y el chatbot consulta los cambios porque lee esas mismas tablas.

## Alcance y comportamiento

- El panel de administración ofrece una entrada activa para cada catálogo.
- Cada catálogo tiene una lista con título, género, plataforma, año, calificación y acciones. Los formularios permiten editar todos los campos de negocio verificados en el esquema.
- El identificador es generado por PostgreSQL y la fecha de registro usa su valor predeterminado; ninguno se puede editar desde el formulario.
- El título es obligatorio. Los campos opcionales vacíos se guardan como `NULL`.
- Se validan longitudes según el esquema real, años y duración como enteros no negativos, y calificación como valor decimal entre 0 y 10 con una cifra decimal como máximo.
- No se fuerza que los títulos sean únicos, ya que el esquema no declara esa restricción.
- La eliminación afecta solo al registro seleccionado, requiere una confirmación visible y usa POST protegido con CSRF.
- Todas las rutas requieren sesión de administrador en el servidor. Los valores SQL se parametrizan y los nombres de tablas/columnas provienen de una lista fija del backend.
- Las operaciones satisfactorias y los errores previsibles se explican en español sin mostrar trazas ni datos internos.
- No se modifica el esquema, no se recargan catálogos al arrancar y no se ejecutan acciones masivas.

## Criterios de aceptación

### AC-1 — Acceso restringido

Un visitante que abre directamente una ruta de catálogo es enviado al login. Un usuario normal recibe acceso denegado. Un administrador puede abrir las listas y realizar operaciones.

### AC-2 — Separación de catálogos

La sección de películas solo muestra y modifica `public.peliculas`; la de videojuegos solo muestra y modifica `public.videojuegos`.

### AC-3 — Listar y consultar

El administrador ve los registros del catálogo elegido y puede abrir un registro para editarlo. La lista no expone campos que no existan en ese catálogo.

### AC-4 — Crear

El administrador puede crear un registro válido. El nuevo registro aparece en la lista, recibe identificador y fecha de PostgreSQL, y no cambia los demás registros.

### AC-5 — Editar

El administrador puede cambiar los campos del registro seleccionado. Tras guardar, los cambios aparecen en la lista y en consultas posteriores del catálogo, sin alterar otros registros.

### AC-6 — Validación

Se rechazan el título vacío, valores numéricos con formato incorrecto o fuera del rango de PostgreSQL, año o duración negativos, calificaciones fuera de 0–10, más de una cifra decimal y textos que exceden el límite del esquema. Los errores se presentan en español y no se guarda el registro inválido.

### AC-7 — Eliminar

La interfaz pide confirmación. Cancelar conserva el registro; confirmar elimina solo ese registro, y las filas restantes se conservan. Una solicitud sin CSRF válido no realiza cambios.

### AC-8 — Preservación de datos

Arrancar la aplicación o abrir las pantallas administrativas no altera ni recarga los catálogos existentes. La implementación no añade migraciones ni acciones masivas.

## Fuera de alcance

- Importación o carga masiva de datos.
- Búsqueda avanzada, filtros de lista, paginación o edición en lote.
- Cambios en el esquema o en el grafo de IA.
- CRUD de conversaciones, mensajes o consumo.

## Supuestos

- Los campos y restricciones son los comprobados en PostgreSQL el 2026-10-05 y resumidos en `AGENTS.md`.
- Los campos `fecha_registro` e identificador son administrados por PostgreSQL.
- El CRUD de la aplicación permite al administrador borrar un registro individual cuando lo confirma; durante desarrollo no se eliminarán registros originales del docente.
