#!/bin/bash
# Script de prueba para GameVault - endpoints de Juego, UserJuego y RAWG
# Uso: bash test_endpoints.sh

BASE="http://localhost:8000/api"

echo "=== 1. Login como admin ==="
ADMIN_TOKEN=$(curl -s -X POST "$BASE/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"axel2026"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access'])")
echo "Token admin obtenido: ${ADMIN_TOKEN:0:20}..."
echo ""

echo "=== 2. Buscar en RAWG (solo admin) ==="
RAWG_BUSQUEDA=$(curl -s "$BASE/juegos/rawg/buscar/?q=elden%20ring" \
  -H "Authorization: Bearer $ADMIN_TOKEN")
echo "$RAWG_BUSQUEDA"
RAWG_ID=$(echo "$RAWG_BUSQUEDA" | python3 -c "import sys,json; print(json.load(sys.stdin)['data'][0]['rawg_id'])")
echo "Primer resultado, rawg_id: $RAWG_ID"
echo ""

echo "=== 3. Detalle de ese juego en RAWG ==="
curl -s "$BASE/juegos/rawg/$RAWG_ID/" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
echo ""
echo ""

echo "=== 4. Crear juego como admin, usando datos de RAWG (deberia dar 201) ==="
NOMBRE_JUEGO="Elden Ring $RANDOM"
JUEGO_RESPONSE=$(curl -s -X POST "$BASE/juegos/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d "{\"rawg_id\":$RAWG_ID,\"nombre\":\"$NOMBRE_JUEGO\",\"genero\":\"RPG, Accion\",\"plataforma\":\"PC, PlayStation 5\",\"descripcion\":\"Un souls-like enorme\",\"fecha_lanzamiento\":\"2022-02-25\",\"imagen_url\":\"https://example.com/portada.jpg\"}")
echo "$JUEGO_RESPONSE"
JUEGO_ID=$(echo "$JUEGO_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
echo "Juego creado con id: $JUEGO_ID"
echo ""

echo "=== 5. Registrar usuario normal ==="
USERNAME_TEST="usuario_$RANDOM"
curl -s -X POST "$BASE/auth/register/" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME_TEST\",\"email\":\"$USERNAME_TEST@test.com\",\"password\":\"test12345\",\"password_confirm\":\"test12345\"}"
echo ""
echo ""

echo "=== 6. Login como usuario normal ==="
USER_TOKEN=$(curl -s -X POST "$BASE/auth/login/" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME_TEST\",\"password\":\"test12345\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['access'])")
echo "Token usuario obtenido: ${USER_TOKEN:0:20}..."
echo ""

echo "=== 7. Usuario normal intenta crear juego (deberia dar 403) ==="
curl -s -w "\nHTTP status: %{http_code}\n" -X POST "$BASE/juegos/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"nombre":"Juego pirata","genero":"Accion","plataforma":"PC"}'
echo ""

echo "=== 8. Usuario normal intenta buscar en RAWG (deberia dar 403) ==="
curl -s -w "\nHTTP status: %{http_code}\n" "$BASE/juegos/rawg/buscar/?q=mario" \
  -H "Authorization: Bearer $USER_TOKEN"
echo ""

echo "=== 9. Usuario normal se une al juego del admin (deberia dar 201) ==="
curl -s -w "\nHTTP status: %{http_code}\n" -X POST "$BASE/juegos/mis-juegos/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d "{\"juego_id\":$JUEGO_ID,\"estado\":\"jugando\"}"
echo ""

echo "=== 10. Ver mi coleccion ==="
curl -s "$BASE/juegos/mis-juegos/" \
  -H "Authorization: Bearer $USER_TOKEN"
echo ""