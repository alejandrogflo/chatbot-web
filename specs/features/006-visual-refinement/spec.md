# F-006 — Refinamiento visual y accesibilidad

**Estado:** Completa
**Incremento:** M3 — Preparación de entrega

## Propósito

Mejorar la claridad, consistencia y presentación de la aplicación web antes de la entrega, usando UI/UX Pro Max como guía de diseño y revisión.

## Alcance

- Instalar en el repositorio la skill UI/UX Pro Max completa con la estructura de proyecto compatible con Codex, incluidas sus referencias, datos y herramienta de búsqueda.
- Generar y guardar un sistema visual apropiado para el chatbot de catálogo y sus páginas administrativas.
- Refinar la navegación, la jerarquía del inicio, el chat, los formularios, las tablas y el resumen de consumo en español.
- Mejorar la adaptación a móvil, los estados de foco y la legibilidad de textos y controles.
- Mantener Flask, Jinja, CSS existente y el comportamiento de rutas; no agregar dependencias de ejecución ni alterar datos o esquema de PostgreSQL.

## Criterios de aceptación

- La skill queda instalada en el repositorio con sus recursos y la búsqueda local puede producir recomendaciones aplicables.
- El sistema visual guardado describe tokens y patrones coherentes con la aplicación existente, sin reemplazar el stack ni imponer estilos irrelevantes.
- Las páginas principales conservan sus recorridos y datos, pero comparten una jerarquía visual coherente; el chat queda como acción principal del usuario.
- El diseño refluye en móvil y escritorio sin perder acciones, etiquetas ni navegación; los controles tienen estados de foco visibles y se revisa el contraste de textos pequeños.
- Se revisan visualmente las páginas modificadas en tamaños móvil y escritorio. Esta revisión no requiere añadir ni ejecutar pruebas automatizadas.
- La documentación de tareas, arquitectura y roadmap refleja el resultado real.

## Límites

- No cambiar autenticación, autorización, privacidad del historial, lógica de chat, consultas SQL ni registro de consumo.
- No modificar los catálogos ni sus registros.
- No incorporar frameworks, paquetes o servicios externos para implementar la interfaz.
- La skill y el documento del sistema visual son herramientas de desarrollo; no son dependencias del proceso web.
