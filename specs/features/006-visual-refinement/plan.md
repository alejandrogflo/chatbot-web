# Plan — F-006 Refinamiento visual y accesibilidad

## Diseño

1. Instalar UI/UX Pro Max en el repositorio mediante el instalador oficial para Codex, sin añadirlo a las dependencias de la aplicación.
2. Consultar el generador local para un chatbot de catálogo audiovisual con panel administrativo y CSS existente; revisar la salida y guardarla como sistema visual del proyecto.
3. Consolidar los estilos compartidos de las páginas Flask y mejorar navegación, jerarquía, tipografía, controles, tablas, estados vacíos y visualización de consumo con HTML/CSS.
4. Mantener el tono en español, la paleta verde ya presente, la semántica HTML y la autorización en servidor. No añadir animación o adornos que oculten información o afecten la accesibilidad.
5. Iniciar la aplicación y revisar visualmente recorridos existentes en una vista móvil y una de escritorio; reparar los defectos visibles.

## Secuencia de implementación

1. Instalar la skill y registrar la recomendación de diseño.
2. Implementar el refinamiento en templates y CSS sin modificar rutas ni contratos de backend.
3. Completar la lista de tareas, anotar las decisiones de presentación en arquitectura y cerrar el incremento en el roadmap.

## Verificación

- Inspeccionar `git diff` para confirmar que el cambio se limita a la skill, documentación y presentación.
- Revisar manualmente el resultado renderizado en resoluciones representativas de móvil y escritorio.
- No ejecutar suites automatizadas; este incremento visual no introduce lógica de servidor.
