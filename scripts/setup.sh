#!/bin/bash
# Primera vez que se levanta el proyecto en esta máquina.
set -e

echo "=== Dando permisos de ejecución a los scripts ==="
chmod +x scripts/*.sh

echo "=== Levantando y construyendo contenedores (las migraciones corren solas) ==="
docker compose up -d --build

echo ""
read -p "¿Crear un superusuario para entrar al panel de Django (/admin)? (s/n) " crear_su
if [ "$crear_su" = "s" ]; then
  docker compose exec backend python manage.py createsuperuser
fi

echo ""
read -p "¿Sembrar datos de prueba (15 juegos + 50 usuarios)? (s/n) " sembrar
if [ "$sembrar" = "s" ]; then
  ./scripts/seed_data.sh
fi

echo ""
echo "Listo. De acá en adelante, para levantar el proyecto alcanza con:"
echo "  docker compose up -d"