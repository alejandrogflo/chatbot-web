# F-001 — Aplicación web y autenticación

**Estado:** Completa; recorridos principales revisados manualmente el 2026-10-05
**Prioridad:** Necesaria para habilitar el acceso privado y los siguientes módulos  
**Depende de:** M1 (base PostgreSQL de soporte), ya disponible

## Problema

La consulta del catálogo y el grafo de IA existen como flujo de desarrollo, pero aún no hay una aplicación web que autentique a las personas y proteja las funciones privadas.

## Resultado esperado

Una persona con cuenta puede iniciar sesión y cerrar sesión en la aplicación web. Las páginas protegidas requieren sesión; las operaciones reservadas se limitan al rol administrador. Como el alta pública no forma parte del curso, debe existir un procedimiento controlado para crear la primera cuenta administradora.

## Historias incluidas

- Como administrador inicial, quiero crear mi cuenta sin una contraseña predeterminada compartida para poder iniciar y administrar el sistema.
- Como usuario registrado, quiero iniciar y cerrar sesión para usar la aplicación con mi identidad.
- Como usuario sin sesión, quiero recibir una invitación clara a iniciar sesión cuando intente abrir una página privada.
- Como usuario normal, no quiero poder acceder a páginas administrativas, incluso si navego directamente a su URL.

## Criterios de aceptación

### AC-1 — Aprovisionamiento inicial

Dado que todavía no hay una cuenta administradora, una persona que opera el entorno local puede crear el primer administrador con nombre, correo y contraseña proporcionados durante el proceso. El procedimiento no usa una contraseña compartida ni deja la contraseña en argumentos persistentes de terminal.

### AC-2 — Correo único

El correo se normaliza antes de guardarse. Dos cuentas no pueden diferir solo por mayúsculas/minúsculas en el correo.

### AC-3 — Contraseña almacenada de forma segura

La cuenta se guarda con un hash de contraseña, nunca con el valor original. Se rechazan contraseñas de menos de 10 caracteres.

### AC-4 — Inicio de sesión

Con correo y contraseña válidos, el usuario entra a una página privada. Si las credenciales no son válidas, se muestra un error genérico que no revela si el correo existe.

### AC-5 — Acceso anónimo

Una persona sin sesión que intenta abrir una página protegida es enviada al inicio de sesión. Tras autenticarse, puede volver a la página que intentó abrir, si es una ruta interna permitida.

### AC-6 — Autorización administrativa

Un administrador autenticado puede abrir la página reservada de administración. Un usuario normal recibe una respuesta de acceso denegado y no ve ni ejecuta operaciones administrativas. La autorización ocurre en el servidor.

### AC-7 — Cierre de sesión

Al cerrar sesión se invalida la sesión. El navegador vuelve a la pantalla pública/de acceso y las páginas privadas vuelven a exigir autenticación.

### AC-8 — Errores de configuración

Si falta la configuración requerida para iniciar la aplicación en el entorno correspondiente, se explica el problema sin exponer secretos. El acceso al chat con IA no se simula en este incremento.

## Fuera de alcance de F-001

- CRUD web de usuarios (F-002).
- CRUD de catálogos (F-003).
- Chat, historial y registro de consumo en la web (F-004 y F-005).
- Registro público, recuperación de contraseña y proveedores OAuth.

## Supuestos

- Los roles válidos son `usuario` y `admin`, de acuerdo con el esquema existente.
- La tabla `usuarios` ya existe y utiliza `password_hash`.
- El primer administrador se crea por un procedimiento local operado por quien ejecuta la aplicación.
- La interfaz y los mensajes están en español.
