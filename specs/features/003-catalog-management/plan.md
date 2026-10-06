# Plan — F-003 Administración de películas y videojuegos

## Diseño

1. Añadir un repositorio de catálogos con una configuración constante para `peliculas` y `videojuegos`. Cada entrada define tabla, identificador, columnas editables, etiquetas, tipo de campo y límite de longitud según PostgreSQL.
2. Mantener una sola capa de rutas Flask para ambas secciones bajo `/admin/catalogos/<catalogo>/`, con listas, alta, edición y eliminación por identificador.
3. Aplicar `admin_required` a cada ruta. Las operaciones que cambian datos se ejecutan mediante POST y heredan la validación CSRF del decorador.
4. Construir SQL únicamente con identificadores tomados del mapa interno fijo; enviar todos los valores de formulario como parámetros Psycopg.
5. Convertir valores opcionales vacíos a `NULL`. Validar título, texto, enteros y calificación antes de llamar al repositorio; no exponer errores de PostgreSQL.
6. Crear plantillas compartidas de lista y formulario, con etiquetas en español, mensajes de error por campo y confirmación para eliminar un registro.
7. Activar enlaces de películas y videojuegos en el panel administrativo y conservar usuarios como sección existente.
8. Registrar en arquitectura y roadmap las decisiones y el resultado cuando el incremento esté completo.

## Límites técnicos

- No añadir dependencias ni migraciones. No cambiar `public.peliculas` ni `public.videojuegos`.
- No editar identificadores ni fechas de registro desde el formulario.
- No usar SQL generado por el modelo ni interpolar valores recibidos del navegador.
- No realizar cambios sobre registros de catálogo durante el trabajo. La eliminación queda disponible como acción individual de la aplicación, protegida y confirmada.
- La validación de interfaz no sustituye la autorización ni la validación del servidor.

## Verificación

A petición del usuario, se ejecutó una comprobación de integración puntual con Flask test client y PostgreSQL local. Cubrió acceso anónimo y de usuario normal, acceso administrador, formularios, validación, CSRF y CRUD en ambas tablas usando únicamente registros temporales que se eliminaron al terminar. No se añadió una suite permanente de pruebas.

Los conteos al inicio y al final de la comprobación de integración fueron 50 películas y 68 videojuegos. El usuario aclaró que había eliminado intencionalmente un videojuego desde el CRUD para probar F-003, lo que explica la diferencia con las 69 filas verificadas el 4 de octubre y anotadas en `AGENTS.md`. La comprobación solo creó y limpió filas temporales; el registro eliminado por el usuario se dejó sin restaurar.
