#!/bin/bash
# Script de prueba para GameVault - endpoints de Juego y UserJuego
# Uso: bash test_endpoints.sh

BASE="http://localhost:8000/api"

echo "=== 1. Login como admin ==="
ADMIN_TOKEN=$(curl -s -X POST "$BASE/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"axel2026"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access'])")
echo "Token admin obtenido: ${ADMIN_TOKEN:0:20}..."
echo ""

echo "=== 2. Crear juego como admin (deberia dar 201) ==="
NOMBRE_JUEGO="Elden Ring $RANDOM"
JUEGO_RESPONSE=$(curl -s -X POST "$BASE/juegos/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d "{\"nombre\":\"$NOMBRE_JUEGO\",\"genero\":\"RPG\",\"plataforma\":\"PC\",\"descripcion\":\"Un souls-like enorme\",\"anio\":2022}")
echo "$JUEGO_RESPONSE"
JUEGO_ID=$(echo "$JUEGO_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
echo "Juego creado con id: $JUEGO_ID"
echo ""

echo "=== 3. Registrar usuario normal ==="
USERNAME_TEST="usuario_$RANDOM"
curl -s -X POST "$BASE/auth/register/" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME_TEST\",\"email\":\"$USERNAME_TEST@test.com\",\"password\":\"test12345\",\"password_confirm\":\"test12345\"}"
echo ""
echo ""

echo "=== 4. Login como usuario normal ==="
USER_TOKEN=$(curl -s -X POST "$BASE/auth/login/" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME_TEST\",\"password\":\"test12345\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['access'])")
echo "Token usuario obtenido: ${USER_TOKEN:0:20}..."
echo ""

echo "=== 5. Usuario normal intenta crear juego (deberia dar 403) ==="
curl -s -w "\nHTTP status: %{http_code}\n" -X POST "$BASE/juegos/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"nombre":"Juego pirata","genero":"Accion","plataforma":"PC","anio":2024}'
echo ""

echo "=== 6. Usuario normal se une al juego del admin (deberia dar 201) ==="
curl -s -w "\nHTTP status: %{http_code}\n" -X POST "$BASE/juegos/mis-juegos/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d "{\"juego_id\":$JUEGO_ID,\"estado\":\"jugando\"}"
echo ""

echo "=== 7. Ver mi coleccion ==="
curl -s "$BASE/juegos/mis-juegos/" \
  -H "Authorization: Bearer $USER_TOKEN"
echo ""