# F-005 — Registro y gráfica de consumo

**Estado:** Completa
**Roadmap:** F-005

## Historia

Como usuario autenticado, quiero consultar cuánto consumo aproximado generaron mis preguntas, separado por películas y videojuegos, para entender el uso de la IA desde mi propia cuenta.

## Alcance

- Guardar por cada intercambio el total académico de palabras procesadas que reporta el grafo, el total de tokens reales del proveedor cuando esté disponible, el usuario, la conversación y la categoría.
- Insertar mensajes e información de consumo dentro de la misma transacción de PostgreSQL.
- Registrar también consultas que no llegaron a identificar categoría. Su categoría queda sin asignar y su consumo académico puede ser cero si el grafo no alcanzó a procesar texto con IA.
- Añadir una página protegida `/consumo` con agregados exclusivos del usuario autenticado, total académico, total del proveedor y una gráfica que separe películas y videojuegos; mostrar aparte el consumo sin categoría.
- Explicar en la interfaz que el conteo académico considera cada palabra como un token y es una aproximación.
- Enlazar el resumen desde la navegación y el inicio del usuario.

## Fuera de alcance

- Cambiar el flujo LangGraph, prompts, proveedor o definición del conteo académico.
- Registrar para preguntas ejecutadas desde la CLI o el evaluador; F-005 cubre los intercambios persistidos por la aplicación web.
- Añadir dependencias de gráficos o telemetría.
- Modificar los catálogos existentes, agregar CRUD administrativo de consumo o exponer agregados de otros usuarios.

## Criterios de aceptación

1. Al completar una consulta web se guardan sus mensajes y exactamente un registro de consumo vinculado al mismo usuario y conversación.
2. El consumo académico y el consumo real del proveedor se conservan en columnas distintas; el segundo puede ser cero cuando el proveedor no reporta uso.
3. Una consulta ambigua o que falla antes de conocer la categoría conserva un registro con categoría nula y no se atribuye a películas ni videojuegos.
4. La ruta `/consumo` requiere sesión y solo muestra agregados del usuario autenticado; no permite consultar los agregados de otra cuenta mediante parámetros.
5. La página muestra barras diferenciadas para películas y videojuegos, un total por categoría y explica el conteo académico por palabras. Si no hay consultas, muestra un estado vacío útil.
6. La migración aditiva permite categorías nulas sin cambiar las categorías válidas existentes ni tocar `peliculas` o `videojuegos`.

## Supuestos y pregunta resuelta

- Para cumplir “registrar el consumo de cada consulta” incluso cuando no haya categoría, la columna `categoria` pasa a admitir `NULL`. Esos registros aparecen como “Sin categoría” fuera de las dos categorías del catálogo.
- Los totales académicos incluyen las palabras contadas por el grafo en prompts y respuesta generada. Si el modelo no llega a devolver uso, el valor registrado es cero; no se estima uso que no se observó.
