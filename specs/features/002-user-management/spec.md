# F-002 — Administración de usuarios

**Estado:** Completa; recorridos principales revisados manualmente el 2026-10-05

**Prioridad:** Necesaria para que el administrador gestione las cuentas de la aplicación

**Depende de:** F-001 (autenticación y autorización administrativa)

## Problema

El panel de administración ya distingue administradores y usuarios, pero todavía no permite gestionar las cuentas guardadas en `public.usuarios`.

## Resultado esperado

Un administrador puede consultar, crear, editar y eliminar cuentas desde la web. Las operaciones se autorizan en el servidor. Los usuarios normales no pueden consultar ni modificar cuentas administrativas.

## Alcance y comportamiento

- La lista muestra identificador, nombre, correo, rol y fecha de registro. Nunca muestra `password_hash`.
- Al crear una cuenta se requieren nombre, correo, contraseña y rol (`usuario` o `admin`). El correo se recorta y normaliza a minúsculas; debe ser válido y único sin distinguir mayúsculas. La contraseña debe tener al menos 10 caracteres y se guarda como hash seguro.
- Al editar se pueden cambiar nombre, correo y rol. La contraseña es opcional: si se deja vacía, se conserva el hash actual; si se proporciona, debe cumplir el mínimo y se reemplaza por un hash nuevo.
- La eliminación se confirma explícitamente desde la interfaz. La página advierte que borrar una cuenta elimina en cascada sus conversaciones, mensajes y consumos asociados, según las claves foráneas existentes.
- No se permite que un administrador elimine su propia cuenta ni que elimine o desactive la última cuenta con rol `admin`.
- Todos los formularios que cambian datos incluyen protección CSRF. Las consultas son parametrizadas y no se envían hashes ni contraseñas a la interfaz.
- Los errores por correo duplicado, datos inválidos, cuenta inexistente o protección de la última cuenta administradora se explican en español.

## Criterios de aceptación

### AC-1 — Acceso restringido

Las rutas de listado, creación, edición y eliminación requieren una sesión de administrador. Un visitante es enviado al login y un usuario normal recibe acceso denegado, incluso al solicitar directamente una ruta.

### AC-2 — Listado seguro

El administrador puede ver las cuentas registradas y sus datos administrativos, sin que `password_hash` aparezca en la respuesta HTML.

### AC-3 — Crear cuenta

El administrador puede crear una cuenta con nombre, correo, contraseña y rol válidos. El nuevo registro aparece en la lista y la contraseña queda guardada como hash.

### AC-4 — Validación de correo

Se rechazan correos vacíos o inválidos y duplicados que solo difieran por mayúsculas/minúsculas. La cuenta existente no se modifica por un error de unicidad.

### AC-5 — Editar cuenta

El administrador puede cambiar nombre, correo o rol. Una contraseña vacía conserva la actual; una contraseña nueva válida se almacena como hash.

### AC-6 — Roles permitidos

Solo se aceptan `usuario` y `admin`. Un administrador no puede quitarse a sí mismo el rol `admin` desde esta pantalla.

### AC-7 — Eliminar cuenta y conservar acceso

La eliminación usa una solicitud POST protegida con CSRF y requiere confirmación en la interfaz. No se puede eliminar la cuenta en sesión ni la última cuenta administradora. Para otras cuentas, la interfaz informa que el historial asociado también se eliminará.

### AC-8 — Mensajes y errores

Los formularios conservan los valores no sensibles cuando hay errores y nunca repueblan contraseñas. Las operaciones completadas y los errores previsibles presentan mensajes en español sin exponer detalles internos.

## Fuera de alcance

- Registro público de cuentas.
- Recuperación de contraseña, OAuth o cambio autónomo de contraseña por el usuario.
- CRUD de catálogos, conversaciones, mensajes o consumo.
- Paginación, búsqueda avanzada o auditoría de cambios.

## Supuestos

- La tabla `public.usuarios` existente es la fuente de verdad y sus columnas son las verificadas en PostgreSQL.
- El índice único existente sobre `LOWER(correo)` aplica la unicidad sin distinguir mayúsculas.
- Los roles válidos en PostgreSQL son `usuario` y `admin`.
- No se requiere una migración nueva para este incremento.
