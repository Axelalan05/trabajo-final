# 🎮 GameVault — Tu biblioteca personal de videojuegos

**GameVault** es una aplicación web pensada para que cualquier usuario pueda armar y gestionar su propia colección de videojuegos. La idea es simple: guardar los juegos que jugaste, los que querés jugar, calificarlos, escribir reseñas y chusmear lo que tienen otros.

El objetivo del proyecto es demostrar un desarrollo fullstack completo: backend con API, frontend moderno, manejo de usuarios, base de datos y despliegue usando contenedores.

---

# 🧱 Stack y arquitectura

## 🔙 Backend

- Django
- Django REST Framework
- SimpleJWT (autenticación con tokens)
- django-cors-headers
- django-filter
- Pillow

## 🔜 Frontend

- Vue 3
- Vue Router
- Pinia (estado global)
- Axios
- Vite

## 🐳 Infraestructura

- Dockerfile (backend y frontend)
- Docker Compose (para levantar todo junto)
- Servicios:
  - Backend (API)
  - Frontend
  - Base de datos (PostgreSQL)

## 🧪 Testing y desarrollo

- Postman (para testear endpoints y validar la API REST durante el desarrollo)

---

# ⚙️ Funcionalidades propuestas

## 🔐 Auth

- Registro con email + contraseña, con email de confirmación (usando `send_mail` de Django + SMTP simple, sin colas — va sincrónico, suficiente para este trabajo final)
- Login/logout con JWT (access + refresh token)
- Perfil de usuario editable (avatar, bio, nombre)
- Recuperación de contraseña por email

---

## 🎮 CRUD principal — Juegos en la colección

- Agregar un juego con:
  - nombre
  - género
  - plataforma
  - imagen de portada
  - descripción
  - año
- Editar y eliminar
- Marcar estado:
  - Jugando
  - Completado
  - Pendiente
  - Abandonado
- Puntaje personal (1–10)
- Reseña / notas personales

---

## 🔍 Exploración

- Listado público de juegos cargados por todos los usuarios
- Búsqueda y filtros (por género, plataforma, estado)
- Ver el perfil público de otro usuario con su colección
- Ordenar por:
  - puntaje
  - fecha de agregado
  - nombre

---

## ⭐ Extra que suma sin complicar

- Favoritos (muchos a muchos entre usuario y juego)
- Estadísticas del perfil:
  - cuántos juegos completados
  - promedio de puntaje
  - géneros más jugados  
    _(todo calculado en el backend, sin usar celery)_
- Paginación en los listados

---

# 📘 Historias de usuario + visión del creador

---

## Épica 1 — Autenticación

**Como creador del sistema**, quiero que el acceso esté protegido y bien gestionado para que cada usuario tenga su información segura.

- US-01 Como visitante, quiero registrarme con email y contraseña para crear mi cuenta.
- US-02 Como visitante, quiero recibir un email de confirmación para activar mi cuenta.
- US-03 Como visitante, quiero iniciar sesión y obtener un token JWT para acceder a mis datos.
- US-04 Como usuario, quiero cerrar sesión invalidando mi refresh token.
- US-05 Como usuario, quiero recuperar mi contraseña si me la olvido.

---

## Épica 2 — Perfil

**Como creador del sistema**, quiero que cada usuario tenga identidad propia dentro de la plataforma y pueda mostrarse al resto.

- US-06 Como usuario, quiero ver y editar mi perfil (nombre, bio, avatar).
- US-07 Como visitante, quiero ver el perfil público de otros usuarios.

---

## Épica 3 — Mi colección

**Como creador del sistema**, quiero que cada usuario pueda gestionar su biblioteca de forma clara y completa.

- US-08 Como usuario, quiero agregar un juego a mi colección.
- US-09 Como usuario, quiero editar la información de un juego.
- US-10 Como usuario, quiero eliminar un juego.
- US-11 Como usuario, quiero marcar el estado de cada juego.
- US-12 Como usuario, quiero poner puntaje y escribir una reseña.

---

## Épica 4 — Exploración

**Como creador del sistema**, quiero que los usuarios puedan descubrir contenido y ver qué juegan otros.

- US-13 Como visitante, quiero ver juegos cargados en la plataforma.
- US-14 Como usuario, quiero buscar juegos por distintos criterios.
- US-15 Como usuario, quiero ordenar resultados.
- US-16 Como usuario, quiero marcar juegos como favoritos.

---

## Épica 5 — Estadísticas

**Como creador del sistema**, quiero mostrar información útil que le dé valor a la colección del usuario.

- US-17 Como usuario, quiero ver estadísticas de mi colección.

---

# 🚫 Alcance (lo que NO se incluye)

Para no irse de tema y mantenerlo manejable:

- Nada de chat
- Nada de notificaciones en tiempo real
- Nada de APIs externas
- Nada de sistema de amigos
- Nada de colas tipo Celery o Redis

---

# 💡 Idea general

Es un proyecto bien completo pero realista. Tiene:

- CRUD
- Auth
- API REST
- Frontend moderno
- Base de datos
- Docker
