# Plan — F-001 Aplicación web y autenticación

**Estado:** En curso
**Especificación:** [spec.md](spec.md)

## Enfoque

Crear la aplicación Flask con un punto de entrada claro, configuración de sesión desde el entorno, vistas básicas en español y una capa de persistencia de usuarios. Implementar hash/verificación de contraseñas, aprovisionamiento local del primer administrador, login/logout y controles reutilizables para rutas autenticadas y administrativas.

Mantener la funcionalidad actual de CLI y del grafo de chat. No trasladar consultas SQL ni llamadas al proveedor de IA a las rutas Flask.

## Secuencia de solicitud

1. Flask recibe la solicitud.
2. Una función compartida carga la cuenta asociada a la sesión.
3. Los decoradores/controles del servidor aplican el requisito de autenticación y, cuando corresponda, el rol administrador.
4. La vista valida la entrada y delega la operación a la capa de aplicación/repositorio.
5. La respuesta presenta el resultado en español; los errores internos se registran sin mostrar trazas ni secretos.

## Decisiones de implementación

- Usar una fábrica de aplicación Flask para configuración explícita y facilitar el crecimiento de rutas.
- Guardar solo el identificador de usuario en la sesión firmada; cargar el estado y rol actuales desde PostgreSQL al autorizar cada solicitud.
- Normalizar correo con espacios eliminados y minúsculas, en concordancia con el índice único existente.
- Usar utilidades de hashing seguras de Werkzeug, disponible con Flask.
- Validar la contraseña con mínimo de 10 caracteres tanto al crear el administrador como en futura alta administrativa.
- Implementar aprovisionamiento con un comando local `create-admin` que solicite la contraseña de forma oculta y se niegue a crear otro administrador inicial si ya existe uno. Las cuentas administrativas posteriores se crean mediante F-002.
- Requerir protección CSRF para formularios que cambian estado. Usar tokens ligados a la sesión y validar en el servidor, sin añadir dependencia para este incremento.
- Configurar cookies de sesión HttpOnly y SameSite; activar Secure cuando la aplicación se ejecute detrás de HTTPS. Nunca usar una clave de sesión fija para un entorno compartido.
- Al redirigir tras el login, aceptar solo rutas internas para evitar redirecciones abiertas.
- Aplicar mensajes de login genéricos para credenciales inválidas y errores de acceso diferenciados para rutas administrativas.

## Datos leídos/escritos

F-001 solo utiliza `public.usuarios`: identificador, nombre, correo, `password_hash`, rol y fecha de registro. No altera tablas de catálogo ni las tablas de conversación.

## Riesgos y respuestas

- **No hay administrador inicial:** incluir el comando de aprovisionamiento local como parte del incremento.
- **La clave de sesión no está configurada:** fallar con mensaje de configuración claro para entornos que exigen secreto; documentar el valor solo en archivo local ignorado por Git.
- **Cambio de rol después de login:** obtener el rol actual de PostgreSQL al autorizar, en vez de confiar en una copia antigua guardada en la sesión.
- **Inyección/abuso en formularios:** validar campos, usar consultas parametrizadas, token CSRF y mensajes de error sin detalles internos.

## Cómo considerar completo el incremento

Todos los criterios AC-1 a AC-8 de la especificación se satisfacen, las tareas están marcadas como completas y README explica configuración, aprovisionamiento del primer administrador y arranque de Flask.
