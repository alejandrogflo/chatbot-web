PROYECTO FINAL

SISTEMA WEB DE CHATBOT DE PELÍCULAS Y
VIDEOJUEGOS

Descripción del Proyecto

Desarrollar una aplicación web que permita a los usuarios iniciar sesión y realizar
consultas sobre películas y videojuegos mediante un chatbot integrado con
Inteligencia Artificial.

Los usuarios serán creados previamente por el administrador. El sistema deberá
consultar  información  almacenada  en  una  base  de  datos  y  enviar  los  datos
relevantes al modelo de IA para generar una respuesta en lenguaje natural. Cada
pregunta  será  procesada  de  forma  independiente;  no  se  requiere  memoria
conversacional.  Sin  embargo,  cada  pregunta  y  respuesta  deberá  almacenarse
para formar el historial del usuario.

La  aplicación  deberá  integrar  Frontend,  Backend,  Base  de  Datos,  SQL  e
Inteligencia Artificial en una aplicación web funcional.

Tecnologías

La tecnología es de elección libre.

•  Frontend: HTML5, CSS3, JavaScript, framework opcional.
•  Backend:  Python,
lenguaje/framework.

Java,  PHP,  C#,

JavaScript/Node.js,

otro

•  Base de datos: PostgreSQL, MySQL/MariaDB, SQL Server, SQLite, otra.

MÓDULOS

1. Usuarios

Funcionalidades

Inicio de sesión.
•
•  Cierre de sesión.
•  Manejo de usuario normal y administrador.

•  El administrador será responsable de crear y gestionar los usuarios mediante

CRUD.

Validaciones

•  Campos obligatorios.
•  Formato de correo.
•  Contraseña mínima.
•  Correo no duplicado.
•  Control de acceso según el usuario.

2. Chat

El usuario podrá realizar preguntas sobre las películas y videojuegos almacenados
en la base de datos.

Ejemplos:

•  ¿Cuáles son 3 películas de drama?
•  ¿Cuáles son 2 videojuegos de aventura?
•  ¿Qué juegos de disparos tienen una calificación mayor a 8.5?

Funcionamiento

Pregunta → Consulta SQL → Datos relevantes → Modelo de IA → Respuesta

Cada pregunta será independiente.

No se requiere memoria conversacional.

3. Historial

Cada pregunta y respuesta deberá almacenarse en la base de datos.

El  usuario  podrá  consultar  únicamente  su  propio  historial,  presentado  en  una
tabla.

Como mínimo:

•  Fecha
•  Pregunta

•  Respuesta

4. Consumo de tokens

Para efectos del proyecto:

Cada palabra procesada se considerará como un token.

El sistema deberá registrar el consumo de cada consulta.

El usuario podrá visualizar su consumo en tokens utilizados mediante una gráfica
de barras, diferenciando:

•  Películas
•  Videojuegos

5. Administración

El administrador será el encargado de mantener la información del sistema.

Deberá contar con una opción adicional en el menú para realizar:

•  CRUD de la tabla usuarios
•  CRUD de la tabla peliculas
•  CRUD de la tabla videojuegos

tablas  conversaciones,  mensajes  y  consumo_tokens  serán  administradas

Las
automáticamente por la aplicación y no requieren un CRUD administrativo.

BASE DE DATOS

Las siguientes tablas son el mínimo requerido:

usuarios

•  id_usuario
•  nombre
•  correo
•  password

•  rol (usuario o admin)
•  fecha_registro

peliculas

•  id_pelicula
•  titulo
•  genero
•  plataforma
•  anio_lanzamiento
•  calificacion
•  director
•  actores
•  productora
•  duracion_minutos
•  clasificacion
•  fecha_registro

videojuegos

•  id_videojuego
•  titulo
•  genero
•  plataforma
•  anio_lanzamiento
•  calificacion
•  desarrollador
•  jugadores
•  fecha_registro

conversaciones

•  id_conversacion
•  id_usuario
•  fecha_creacion

mensajes

•  id_mensaje
•  id_conversacion
•  rol
•  contenido
•  fecha

consumo_tokens

•  id_consumo
•  id_usuario
•  categoria

•  tokens
•  fecha

Las  tablas  peliculas  y  videojuegos  serán  proporcionadas  por  el  docente  con  datos
iniciales. El estudiante deberá implementar las tablas restantes y sus relaciones.

ENTREGABLES

1.  Código fuente

Frontend y backend organizados, cumpliendo con los requerimientos
indicados.
2.  Script SQL

Creación de tablas y relaciones.

3.  Video demostrativo

Entre 2 y 3 minutos mostrando el funcionamiento.

CONSIDERACIONES GENERALES

Los módulos y funcionalidades descritos anteriormente representan los requisitos
mínimos del proyecto.

La  aplicación  deberá  presentar  una  interfaz  clara,  agradable  y  fácil  de  utilizar,
aplicando los principios de UX y diseño de interfaces vistos durante el seminario.
En  particular,  la  interfaz  del  chatbot  deberá  tomar  como  referencia las  interfaces
actuales de aplicaciones como ChatGPT, Gemini y otros asistentes de IA.

También se deberán considerar aspectos básicos de arquitectura, organización del
código, seguridad, validaciones, manejo de errores y buenas prácticas de desarrollo
web.

Cualquier  funcionalidad  adicional,  mejora  de  diseño,  característica  técnica  o
esfuerzo adicional que mejore la aplicación será tomado en cuenta en la evaluación
del proyecto.

Valor: 6 pts.

Fecha de entrega: 05 de octubre hasta las 23:59 hrs.


