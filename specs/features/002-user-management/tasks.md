# Tareas — F-002 Administración de usuarios

**Estado:** Implementación inicial completada; falta revisión en ejecución

**Especificación:** [spec.md](spec.md)

**Plan:** [plan.md](plan.md)

- [x] Consultar los documentos de producto, arquitectura y el esquema real de `public.usuarios`.
- [x] Definir alcance, criterios de aceptación, plan y secuencia de implementación.
- [x] Añadir al repositorio las consultas parametrizadas de lista, búsqueda administrativa, alta, actualización y eliminación.
- [x] Proteger las operaciones con autorización administrativa y CSRF.
- [x] Implementar validación de nombre, correo, rol y contraseñas para alta/edición.
- [x] Evitar eliminar la propia cuenta, degradar la propia cuenta admin o quitar la última cuenta administradora.
- [x] Implementar páginas de listado y formulario de alta/edición en español.
- [x] Mostrar advertencia y confirmación sobre la eliminación en cascada del historial.
- [x] Enlazar el panel de administración al CRUD de usuarios y presentar errores previsibles claramente.
- [x] Registrar en arquitectura y roadmap el diseño y estado de F-002.
- [ ] Revisar AC-1 a AC-8 en ejecución y cerrar F-002.
