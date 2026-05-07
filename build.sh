#!/bin/bash
set -e

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Ejecutando migraciones..."
python manage.py migrate

echo "Colectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "Build completado satisfactoriamente"
