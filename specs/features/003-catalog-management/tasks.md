# Tareas — F-003 Administración de películas y videojuegos

**Estado:** Completa; integración con PostgreSQL verificada el 2026-10-05

**Especificación:** [spec.md](spec.md)

**Plan:** [plan.md](plan.md)

- [x] Consultar producto, arquitectura, esquema real y restricciones de ambos catálogos.
- [x] Definir alcance, criterios de aceptación, plan y límites de preservación de datos.
- [x] Implementar repositorio allowlist con lecturas y escrituras parametrizadas por catálogo.
- [x] Implementar rutas protegidas para lista, creación, edición y eliminación individual.
- [x] Validar campos opcionales, longitudes y valores numéricos según el esquema.
- [x] Crear listas y formularios compartidos en español, con mensajes y confirmación de eliminación.
- [x] Activar las secciones de películas y videojuegos desde el panel administrativo.
- [x] Verificar permisos, validaciones, CSRF y CRUD en ambas tablas con registros temporales; limpiar los registros temporales.
- [x] Confirmar que los conteos iniciales se conservaron y documentar la diferencia preexistente del conteo de videojuegos.
- [x] Actualizar arquitectura, roadmap y README al cerrar F-003.
