#!/bin/bash
set -e

echo "Running migrations..."
poetry run alembic upgrade head

echo "Starting server..."
exec "$@"