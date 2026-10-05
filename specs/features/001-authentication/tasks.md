# Tareas — F-001 Aplicación web y autenticación

**Estado:** Implementación inicial completada; falta revisar en ejecución
**Especificación:** [spec.md](spec.md)  
**Plan:** [plan.md](plan.md)

- [x] Crear fábrica de aplicación Flask y punto de entrada web, conservando los comandos CLI actuales.
- [x] Añadir configuración para secreto de sesión y opciones de cookie por entorno.
- [x] Crear repositorio de usuarios con correo normalizado y consultas parametrizadas.
- [x] Implementar hash y verificación de contraseña con el campo existente `password_hash`.
- [x] Implementar comando local para crear el primer administrador con captura oculta de contraseña y validaciones.
- [x] Implementar login y logout con mensajes genéricos de credenciales inválidas.
- [x] Implementar carga de identidad desde sesión y controles servidor para usuario autenticado y administrador.
- [x] Proteger formularios mutables con tokens CSRF y limitar redirecciones de retorno a rutas internas.
- [x] Añadir páginas mínimas en español para login, inicio privado y acceso denegado.
- [x] Actualizar README con configuración web, comando de primer administrador y forma de iniciar Flask.
- [ ] Revisar AC-1 a AC-8 en ejecución y cerrar el incremento.
