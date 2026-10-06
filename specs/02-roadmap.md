# Roadmap de implementación

El orden prioriza dependencias y entrega incrementos visibles. Los estados reflejan lo que existe hoy en el repositorio, no solo lo que está documentado.

| ID | Incremento | Estado | Evidencia / siguiente resultado |
|---|---|---|---|
| M0 | Requisitos, arquitectura y flujo SDD | Completa | `pf.md`, `AGENTS.md` y esta carpeta `specs/` |
| M1 | Base de datos de soporte y catálogo existente | Completa | Migración aditiva aplicada; no tocar datos de catálogo |
| M2 | Grafo de chat y consulta PostgreSQL | Completa | CLI, grafo LangGraph, consulta parametrizada y evaluador |
| F-001 | Aplicación web, autenticación y autorización por rol | Completa | Recorridos de login/logout, acceso anónimo, roles y credenciales inválidas revisados manualmente por el usuario el 2026-10-05 |
| F-002 | CRUD administrativo de usuarios | Completa | Listado seguro, creación, validaciones, edición, confirmación y eliminación revisados manualmente por el usuario el 2026-10-05 |
| F-003 | CRUD administrativo de películas y videojuegos | Pendiente | Requiere autorización administrativa |
| F-004 | Chat web e historial privado | Pendiente | Integra el grafo existente con persistencia de mensajes |
| F-005 | Registro y gráfica de consumo | Pendiente | Guarda conteo por pregunta y separa categorías |
| M3 | Preparación de entrega | Pendiente | Configuración reproducible, revisión integral y demostración de 2–3 minutos |

## Dependencias

```text
M0 -> M1 -> M2 -> F-001 -> F-002
                         \-> F-003
                         \-> F-004 -> F-005
F-001 + F-002 + F-003 + F-004 + F-005 -> M3
```

F-002, F-003 y F-004 pueden desarrollarse como ciclos separados después de F-001. F-005 depende de que F-004 persista cada consulta.
