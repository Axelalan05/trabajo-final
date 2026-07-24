#!/bin/bash
# Carga el catalogo de prueba: 15 juegos reales via RAWG y 50 usuarios
# (jugador1..jugador50, password seed12345), unidos a los juegos
# segun la distribucion 5 juegos x 4 usuarios + 10 juegos x 3 usuarios.
#
# Requiere que los contenedores esten levantados (bash scripts/setup.sh
# o docker compose up -d) y que RAWG_API_KEY este configurada.
#
# Uso: bash scripts/seed_data.sh

set -e

echo "=== Verificando que el backend este arriba ==="
if ! docker compose ps backend | grep -q "Up"; then
    echo "El contenedor 'backend' no esta corriendo. Levantalo primero con:"
    echo "  bash scripts/setup.sh"
    exit 1
fi

echo "=== Cargando juegos y usuarios de prueba ==="
docker compose exec backend python manage.py seed_data

echo ""
echo "Listo. Podes entrar como cualquier jugador1..jugador50 con password: seed12345"