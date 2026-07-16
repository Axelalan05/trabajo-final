#!/bin/bash
# Borra la base de datos por completo y la reconstruye desde las migraciones actuales
set -e

read -p "Esto borra TODOS los datos de la base. Estas seguro? (s/n) " confirm
if [ "$confirm" != "s" ]; then
  echo "Cancelado."
  exit 0
fi

echo "=== Bajando contenedores y borrando volumenes ==="
docker compose down -v

echo "=== Levantando de nuevo ==="
docker compose up -d

echo "=== Esperando a que la base de datos este lista ==="
until docker compose exec db pg_isready -U postgres > /dev/null 2>&1; do
  echo "Esperando a Postgres..."
  sleep 1
done

echo "=== Aplicando migraciones ==="
docker compose exec backend python manage.py migrate

echo ""
echo "Base reseteada. Recorda crear un superusuario:"
echo "  docker compose exec backend python manage.py createsuperuser"