#!/bin/bash
# Levanta el proyecto completo desde cero (primera vez o después de mucho tiempo sin tocarlo)
set -e

echo "=== Levantando contenedores ==="
docker compose up -d

echo "=== Esperando a que la base de datos este lista ==="
until docker compose exec db pg_isready -U postgres > /dev/null 2>&1; do
  echo "Esperando a Postgres..."
  sleep 1
done

echo "=== Aplicando migraciones ==="
docker compose exec backend python manage.py migrate

echo ""
echo "Todo listo. Si necesitas un superusuario, corre:"
echo "  docker compose exec backend python manage.py createsuperuser"