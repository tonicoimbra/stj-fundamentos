#!/bin/bash
# Script de inicialização do STJ Fundamentos Legais

echo "🔧 Instalando dependências..."
pip install -r requirements.txt --break-system-packages -q

echo "📦 Aplicando migrações..."
python manage.py migrate --run-syncdb

echo "📊 Importando dados..."
python manage.py importar_fundamentos --dir=./data

echo "🚀 Iniciando servidor..."
python manage.py runserver 0.0.0.0:8000
