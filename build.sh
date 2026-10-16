#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Applying database migrations..."
python manage.py migrate

# Optional: Auto-create superuser if environment variables are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "Creating superuser if not exists..."
  python manage.py createsuperuser --noinput || true
fi
