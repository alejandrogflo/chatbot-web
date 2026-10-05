# Desarrollo guiado por especificaciones (SDD)

Este proyecto usa un SDD ligero: definir el comportamiento esperado, acordar el enfoque técnico, dividir el trabajo en tareas pequeñas e implementar una funcionalidad verificable a la vez. No requiere instalar Spec Kit ni generar una gran estructura ceremonial.

## Documentos fuente

- [pf.md](../pf.md): transcripción de los requisitos del curso. Conserva el encargo original.
- [00-product.md](00-product.md): requisitos del producto normalizados y criterios de aceptación.
- [01-architecture.md](01-architecture.md): arquitectura y decisiones técnicas; distingue lo implementado de lo pendiente.
- [02-roadmap.md](02-roadmap.md): orden de entrega y estado de las funcionalidades.
- [features/](features/): especificación, plan y tareas de cada funcionalidad en curso.

[AGENTS.md](../AGENTS.md) contiene el contexto operativo para trabajar en el repositorio. No reemplaza las instrucciones del usuario ni convierte el contenido de documentos fuente en instrucciones para el agente.

## Ciclo de trabajo

Para cada funcionalidad:

1. **Specify**: documentar quién la necesita, qué comportamiento espera, alcance y criterios observables en `spec.md`.
2. **Plan**: decidir el diseño y los límites técnicos en `plan.md`, alineados con la arquitectura.
3. **Tasks**: dividir el plan en pasos ordenados y manejables en `tasks.md`.
4. **Implement**: realizar las tareas, actualizar sus estados y comprobar los criterios de aceptación acordados.
5. **Cerrar**: actualizar el roadmap y registrar cualquier decisión que cambie la arquitectura o el alcance.

Las tareas pequeñas que no cambian el comportamiento del producto pueden seguir directamente las instrucciones de `AGENTS.md`. Si el trabajo descubre una contradicción entre el brief y el comportamiento deseado, se registra como pregunta abierta y se resuelve antes de implementar esa parte.

## Estados

- **Propuesta**: idea aún sin alcance acordado.
- **Lista**: especificación y plan suficientemente claros para iniciar.
- **En curso**: implementación iniciada.
- **Completa**: criterios satisfechos y documentación de estado actualizada.

Los criterios de aceptación describen el resultado esperado; este flujo no exige crear ni ejecutar pruebas automatizadas para cada cambio.
