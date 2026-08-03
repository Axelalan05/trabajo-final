# 🎮 GameVault — Tu biblioteca personal de videojuegos

**GameVault** es una aplicación web para armar y gestionar una colección personal de videojuegos. El catálogo de juegos lo mantengo yo como administrador (cargando cada título desde la API de RAWG, con portada, género, plataformas y fecha de lanzamiento reales) para evitar duplicados y datos inconsistentes. Cualquier usuario registrado puede unirse a los juegos del catálogo, llevar el registro de su propio estado (pendiente, jugando, completado, abandonado), puntuarlos y escribir una reseña personal.

Es mi proyecto final para la materia **Trabajo Final**, en la Universidad Nacional del Comahue.

---

## 🧱 Stack y arquitectura

### Backend

- Django + Django REST Framework
- Autenticación con JWT (`djangorestframework-simplejwt`), con blacklist de tokens
- PostgreSQL
- `django-filter` para los filtros de búsqueda
- `django-cors-headers`
- Envío de emails con **Resend** (confirmación de cuenta y recuperación de contraseña)
- Integración con la **API de RAWG** (rawg.io) para traer portada, descripción, género, plataformas y fecha de lanzamiento de cada juego

### Frontend

- Vue 3 + TypeScript
- Vue Router (con guards de autenticación y de admin)
- Pinia para el estado global
- Axios (con interceptores para inyectar el token y refrescarlo automáticamente)

### Infraestructura

- Docker + Docker Compose, con 4 servicios: `db` (PostgreSQL), `backend` (Django), `frontend` (Vue/Vite), y `nginx` (reverse proxy)
- **nginx** como puerta de entrada única: rutea `/api/`, `/admin/` y `/media/` al backend, y todo lo demás al frontend
- **HTTPS local con mkcert**, sirviendo la app en `https://gamevault.local` con certificado confiable en la máquina (sin advertencias de "sitio no seguro")
- Scripts de conveniencia en `scripts/` (`setup.sh`, `reset_db.sh`, `seed_data.sh`, `test_endpoints.sh`)

### Testing / desarrollo

- Comando de gestión `seed_data` (Django) que carga un catálogo de prueba (desde `fixtures/juegos_seed.json`, resuelto contra RAWG) y usuarios de prueba, reutilizando las mismas validaciones que la API pública
- Scripts de `curl` para probar los endpoints de punta a punta sin necesidad de una herramienta externa

---

## ⚙️ Funcionalidades

### 🔐 Autenticación y cuenta

- Registro con usuario, email y contraseña, con email de confirmación (Resend). En el entorno de desarrollo actual, al no contar todavía con un dominio propio verificado, el plan gratuito de Resend solo permite enviar correos reales a la casilla del titular de la cuenta (`axeldavidalan05@gmail.com`); para cualquier otro usuario, el registro y la solicitud de recuperación de contraseña igual funcionan: el backend devuelve el enlace correspondiente (`verification_url` / `reset_url`) en el JSON de la respuesta, y el frontend lo muestra por `console.log` en la consola del navegador (`RegisterView.vue` y `ForgotPasswordView.vue`), a modo de entorno de prueba.
- Login/logout con JWT (access + refresh token, con blacklist al cerrar sesión)
- Recuperación de contraseña por email (o vía la consola del navegador, según la limitación anterior)
- Perfil propio editable, y perfil público de otros usuarios

### 🎮 Catálogo (solo administrador)

- Alta de juegos buscando directamente en RAWG: se elige un resultado y se autocompletan nombre, portada, descripción, género, plataformas y fecha de lanzamiento
- Edición y baja de juegos del catálogo
- Validación de duplicados por nombre y por ID de RAWG

### 📚 Mi colección (cualquier usuario autenticado)

- Unirse a un juego del catálogo
- Marcar estado: pendiente, jugando, completado o abandonado (con su propio color)
- Puntaje personal (1–10) y reseña
- Salir de un juego (con modal de confirmación)
- Estadísticas propias: juegos completados, puntaje promedio, géneros más jugados

### 🔍 Exploración

- Catálogo público, con filtros por nombre, género y plataforma (incluye abreviaturas de PlayStation: "ps", "ps3", etc.)
- Orden por más recientes o por nombre
- Detalle de cada juego en una vista propia
- Paginación en los listados

### 🛠️ Administración

- Panel propio en Vue para cargar/editar el catálogo (además del admin de Django)
- Gestión de usuarios: búsqueda, ver detalle (con sus juegos y reseñas) y expulsar usuarios

---

## 🚀 Cómo levantarlo en una PC nueva

### 1. Clonar y configurar variables de entorno

```bash
git clone https://github.com/Axelalan05/trabajo-final.git
cd trabajo-final
cp .env-example .env
```

Abrí el `.env` recién creado y completá:

- `RAWG_API_KEY`: se consigue gratis registrándose en [rawg.io/apidocs](https://rawg.io/apidocs)
- `RESEND_API_KEY` y `RESEND_FROM_EMAIL`: credenciales de [resend.com](https://resend.com)
- `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DJANGO_SECRET_KEY`: los que prefieras para tu entorno local
- `FRONTEND_URL`: `https://gamevault.local`

### 2. Certificado HTTPS local con mkcert

La app se sirve en `https://gamevault.local`. Esto requiere generar un certificado **una sola vez por máquina** (no se sube a Git, ya está en `.gitignore` bajo `nginx/certs/`).

#### En Windows (con WSL, como este proyecto)

> Importante: mkcert se instala y corre en **Windows**, no dentro de WSL — el navegador (Chrome/Edge) usa el almacén de certificados de Windows, no el de Linux.

1. Descargar el ejecutable desde [github.com/FiloSottile/mkcert/releases/latest](https://github.com/FiloSottile/mkcert/releases/latest), el archivo que dice `windows-amd64` (ej. `mkcert-v1.4.4-windows-amd64.exe`).
2. Crear la carpeta `C:\mkcert`, mover el archivo descargado ahí adentro, y renombrarlo a `mkcert.exe`.
3. Abrir **PowerShell como Administrador** (menú inicio → buscar "PowerShell" → click derecho → "Ejecutar como administrador") y correr:

```powershell
   cd C:\mkcert
   .\mkcert.exe -install
   .\mkcert.exe gamevault.local
```

Esto crea `gamevault.local.pem` y `gamevault.local-key.pem` en `C:\mkcert`. 4. Copiar esos dos archivos al proyecto, desde la terminal de **WSL**:

```bash
   mkdir -p ~/trabajo-final/nginx/certs
   cp /mnt/c/mkcert/gamevault.local.pem ~/trabajo-final/nginx/certs/
   cp /mnt/c/mkcert/gamevault.local-key.pem ~/trabajo-final/nginx/certs/
```

#### En Linux

```bash
sudo apt update
sudo apt install libnss3-tools wget -y
wget https://github.com/FiloSottile/mkcert/releases/latest/download/mkcert-v1.4.4-linux-amd64
chmod +x mkcert-v1.4.4-linux-amd64
sudo mv mkcert-v1.4.4-linux-amd64 /usr/local/bin/mkcert
mkcert -install
mkdir -p nginx/certs
cd nginx/certs
mkcert gamevault.local
cd ../..
```

(Revisar en la página de releases si hay una versión más nueva que `v1.4.4` y ajustar el número en la URL del `wget`.)

### 3. Archivo hosts

También es un paso único por máquina: le dice al sistema operativo que `gamevault.local` apunta a la propia PC, en vez de salir a buscarlo a internet.

**Windows** (el `hosts` de Windows, no el de WSL — es el que usa el navegador):

1. Abrir el Bloc de notas **como Administrador** (buscarlo en el menú inicio → click derecho → "Ejecutar como administrador").
2. `Archivo → Abrir`, pegar esta ruta en el campo de nombre de archivo (cambiando el filtro a "Todos los archivos" si hace falta):

C:\Windows\System32\drivers\etc\hosts

3. Al final del archivo, agregar:

   127.0.0.1 gamevault.local

4. Guardar con `Ctrl+S`.
5. Verificar desde cualquier terminal:

```bash
   ping gamevault.local
```

Debe resolver a `127.0.0.1`.

**Linux:**

```bash
sudo nano /etc/hosts
```

Agregar la misma línea al final (`127.0.0.1 gamevault.local`), guardar con `Ctrl+O`, `Enter`, y salir con `Ctrl+X`.

### 4. Levantar el proyecto

**Primera vez en esta máquina:**

```bash
./scripts/setup.sh
```

Este script:

- Da permisos de ejecución a todos los scripts de `scripts/`
- Construye y levanta los 4 contenedores (las migraciones se aplican solas al arrancar el backend)
- Pregunta si querés crear un superusuario (para entrar al panel de Django en `/admin` y gestionar usuarios/juegos sin pasar por la API pública)
- Pregunta si querés sembrar datos de prueba: 15 juegos y 50 usuarios (`jugador1`...`jugador50`, contraseña `seed12345`)

**Para desarrollar día a día** (una vez hecho el setup inicial):

```bash
docker compose up -d
```

Nada más — las migraciones se aplican automáticamente en cada arranque si hay pendientes.

### 5. Verificar que todo esté arriba

```bash
docker compose ps
```

Deben figurar 4 contenedores en estado `Up`: `gamevault_db`, `gamevault_backend`, `gamevault_frontend`, `gamevault_nginx`.

### 6. Listo

Entrar a `https://gamevault.local` 🎮 — debería cargar con el candado verde, sin advertencias de "sitio no seguro".

---

## 🚫 Fuera de alcance

Para mantener el proyecto manejable dentro del tiempo de la materia:

- Chat o mensajería entre usuarios
- Notificaciones en tiempo real
- Sistema de amigos/seguidores
- Colas de tareas (Celery, Redis)
