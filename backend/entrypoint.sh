# backend/entrypoint.sh
#!/bin/bash
set -e

echo "=== Aplicando migraciones ==="
python manage.py migrate --noinput

exec "$@"