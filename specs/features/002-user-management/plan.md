# Plan — F-002 Administración de usuarios

**Estado:** En curso

**Especificación:** [spec.md](spec.md)

## Enfoque

Extender el repositorio de usuarios existente con operaciones CRUD parametrizadas y añadir un blueprint Flask protegido con `admin_required`. Las rutas validan los formularios y delegan la persistencia; las plantillas muestran exclusivamente campos administrativos. Se reutilizan el hash de Werkzeug, la validación de correo existente, las protecciones CSRF aplicadas en los decoradores de sesión/autorización y las sesiones de F-001.

## Rutas previstas

- `GET /admin/usuarios/`: listado.
- `GET|POST /admin/usuarios/nuevo`: formulario y creación.
- `GET|POST /admin/usuarios/<id>/editar`: formulario y actualización.
- `POST /admin/usuarios/<id>/eliminar`: eliminación con CSRF.

Cada ruta lleva autorización administrativa en el servidor. La eliminación no usa GET.

## Persistencia

- Añadir consultas para listar, buscar para administración, crear, actualizar y eliminar.
- Seleccionar en las vistas solo `id_usuario`, `nombre`, `correo`, `rol` y `fecha_registro`.
- Dejar que el índice `usuarios_correo_lower_uq` arbitre la unicidad y traducir `UniqueViolation` a un error de formulario.
- Para cambios que afecten al último administrador, bloquear escrituras concurrentes sobre `public.usuarios` dentro de una transacción, contar administradores y rechazar una eliminación o degradación que deje cero.
- Al borrar, confirmar la acción y explicar el efecto `ON DELETE CASCADE` existente; no cambiar el esquema ni borrar otras cuentas relacionadas.

## Interfaz y validación

- Crear tabla/listado y formulario compartido para alta y edición en español.
- Mostrar roles como opciones permitidas; nunca aceptar otros valores.
- En alta, exigir contraseña mínima de 10 caracteres. En edición, campo vacío significa conservar la contraseña; campo no vacío la restablece después de validarlo.
- No rellenar el campo de contraseña tras ningún error ni incluir hashes en el contexto de plantillas.
- Mostrar errores de campo y mensajes flash claros; los fallos de base de datos se registran en el servidor y se muestran sin trazas.
- En el panel administrativo, enlazar la tarjeta “Usuarios” al listado real.

## Datos que no cambian

F-002 usa la tabla `public.usuarios` existente. No requiere migración y no modifica las tablas de películas o videojuegos. Las conversaciones, mensajes y consumos solo se eliminan como consecuencia de las claves foráneas al eliminar una cuenta, con aviso y confirmación.

## Riesgos y respuestas

- **Bloqueo de acceso al sistema:** impedir borrar la propia cuenta o quitar su rol administrador y proteger siempre la última cuenta admin.
- **Eliminación de historial:** mostrar explícitamente la cascada antes de confirmar.
- **Colisión de correo concurrente:** confiar en el índice único de PostgreSQL y mostrar un error sin modificar registros existentes.
- **Exposición de credenciales:** nunca seleccionar `password_hash` en vistas/listados y limpiar el campo de contraseña en cada respuesta.

## Cierre

F-002 se completa cuando AC-1 a AC-8 están implementados, revisados, las tareas están actualizadas y el roadmap refleja el estado. No se requieren pruebas automatizadas para este incremento.
