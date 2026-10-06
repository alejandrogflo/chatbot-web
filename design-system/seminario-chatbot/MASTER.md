# Sistema visual — Seminario Chatbot

**Estado:** Sistema aplicado para F-006
**Interfaz:** Flask + Jinja + HTML/CSS sencillo
**Idioma:** Español
**Producto:** Chat privado para explorar catálogos de películas y videojuegos, con historial, consumo y herramientas administrativas.

## Dirección

Diseño de producto ligero con una presentación editorial del catálogo y patrones sobrios de interfaz conversacional. La pantalla de inicio pone el chat al frente; administración, historial y consumo permanecen a mano como tareas de apoyo. Las páginas administrativas favorecen lectura y operación sobre decoración.

La consulta UI/UX Pro Max `AI chatbot entertainment catalog` relacionó correctamente el producto con **AI-Native UI**; `minimal media catalog interface` encontró **Minimalism & Swiss Style** como sistema apto para aplicaciones, paneles y herramientas. La generación completa no produjo una recomendación fiable para este sitio: devolvió estructuras de landing promocional y paletas oscura/morada fuera de contexto. Por eso esta guía conserva la identidad verde ya presente y usa solo los hallazgos pertinentes de producto, estilo, UX y gráficas.

## Tokens

| Token | Valor | Uso |
|---|---|---|
| `--ink` | `#172421` | Texto principal y encabezados |
| `--muted` | `#52635b` | Texto secundario legible |
| `--green` | `#176b57` | Marca y acción primaria |
| `--green-dark` | `#105342` | Hover y énfasis de marca |
| `--mint` | `#e7f1eb` | Superficies suaves y selección |
| `--paper` | `#f3f7f4` | Fondo de página |
| `--surface` | `#ffffff` | Formularios, paneles y tablas |
| `--line` | `#d7e3dc` | Bordes y divisores |
| `--game` | `#965312` | Barra de videojuegos y señal secundaria |
| `--danger` | `#96392f` | Acciones y mensajes destructivos |

El verde continúa como único color de marca. El ámbar oscuro identifica la serie de videojuegos en la gráfica; siempre se muestra junto a su etiqueta textual. El contraste se calcula sobre las superficies finales y se corrige antes de entregar.

## Tipografía y ritmo

- Usar fuentes del sistema (`ui-sans-serif`, `system-ui`, `-apple-system`, `Segoe UI`, `sans-serif`) para evitar una descarga de fuentes o dependencias externas.
- Texto de cuerpo de al menos 16 px cuando el espacio lo permita, interlineado entre 1.5 y 1.7; mantener las notas pequeñas con contraste suficiente.
- Usar una escala compacta y consistente para títulos, etiquetas, datos y metadatos. Los datos numéricos usan cifras tabulares.
- Mantener un ancho de lectura cercano a 65 caracteres y un contenedor de página de hasta 1200 px.
- Emplear espacios de 4/8 px como base. El movimiento es breve y opcional; respetar `prefers-reduced-motion`.

## Componentes y estados

- Una sola acción primaria por página. El chat es el destino principal del usuario; historial y consumo son enlaces secundarios.
- Navegación superior en el mismo lugar en páginas autenticadas. La página actual se identifica con color, fondo y `aria-current`.
- Usar superficies y bordes solo para agrupar contenido; reserva sombras tintadas para jerarquía real.
- Escala de radios documentada: controles 10 px, paneles 16 px y panel de acceso 22 px; etiquetas de estado pueden ser cápsulas.
- Botones y enlaces operables con teclado, foco visible, etiqueta textual y área cómoda al tocar. No depender de hover.
- Etiquetas visibles en todos los campos; los errores permanecen junto a su campo y los estados vacíos orientan hacia la siguiente acción.
- Evitar símbolos decorativos como sustitutos de nombres de acción y no depender de iconos o color para transmitir significado.

## Adaptación y datos

- Diseñar primero para una columna angosta; mejorar a dos o tres columnas en escritorio con puntos de quiebre consistentes alrededor de 760 y 1024 px.
- En móvil, priorizar chat, navegación, valores y acciones. Las tablas administrativas pueden pasar a filas etiquetadas en tarjetas; el historial conserva preguntas y respuestas completas con ajuste de texto.
- Comparaciones de categorías usan barras horizontales con etiqueta y valor visibles, colores distinguibles y una alternativa textual accesible. No añadir una biblioteca de gráficas.
- Conservar la presentación en español, el tema claro y el comportamiento actual de formularios y rutas.

## Verificaciones antes de entregar

- Revisar foco de teclado, contraste normal mínimo 4.5:1 y controles en viewport de 375, 768, 1024 y 1440 px.
- Confirmar que los textos largos, errores, tablas y controles no se cortan ni provocan desbordamiento de página.
- Revisar el estado normal, hover, foco, presionado, deshabilitado y vacío donde corresponda.
- Mantener la identidad verde, evitar gradientes morados genéricos, glassmorphism, movimiento decorativo y fuentes remotas.
