#!/bin/bash
set -e

echo "🚀 Starting STJ Fundamentos application..."

# Wait for database to be ready
if [ "$DB_ENGINE" = "postgresql" ]; then
    echo "⏳ Waiting for PostgreSQL to be ready..."

    while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" > /dev/null 2>&1; do
        echo "   Waiting for PostgreSQL..."
        sleep 2
    done

    echo "✅ PostgreSQL is ready!"
fi

# Run migrations
echo "🔄 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist
echo "👤 Creating superuser if not exists..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superuser created: admin / admin123')
else:
    print('ℹ️  Superuser already exists')
EOF

# Import data if database is empty
echo "📊 Checking if data needs to be imported..."
python manage.py shell << EOF
from fundamentos.models import FundamentoLegal
import os

if FundamentoLegal.objects.count() == 0:
    print('📥 Database is empty, importing data...')
    if os.path.exists('/app/data'):
        os.system('python manage.py importar_fundamentos --dir=/app/data')
        print('✅ Data imported successfully!')
    else:
        print('⚠️  Data directory not found, skipping import')
else:
    print(f'ℹ️  Database already has {FundamentoLegal.objects.count()} fundamentos')
EOF

echo "✅ Application is ready!"
echo "🌐 Starting web server..."

# Execute the CMD from Dockerfile
exec "$@"
