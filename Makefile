.PHONY: help build up down logs shell migrate collectstatic createsuperuser import-data clean test

help:
	@echo "STJ Fundamentos - Comandos Disponíveis"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make build          - Build Docker image"
	@echo "  make up             - Start containers"
	@echo "  make down           - Stop containers"
	@echo "  make logs           - View logs"
	@echo "  make restart        - Restart containers"
	@echo ""
	@echo "Django Commands:"
	@echo "  make shell          - Open Django shell"
	@echo "  make migrate        - Run migrations"
	@echo "  make collectstatic  - Collect static files"
	@echo "  make createsuperuser - Create superuser"
	@echo "  make import-data    - Import fundamentos data"
	@echo ""
	@echo "Development:"
	@echo "  make dev            - Start local development server"
	@echo "  make test           - Run tests"
	@echo "  make clean          - Clean temporary files"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy         - Build and deploy"
	@echo "  make backup-db      - Backup database"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

restart:
	docker-compose restart

shell:
	docker-compose exec web python manage.py shell

bash:
	docker-compose exec web bash

migrate:
	docker-compose exec web python manage.py migrate

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

import-data:
	docker-compose exec web python manage.py importar_fundamentos --dir=/app/data

dev:
	python manage.py runserver

test:
	python manage.py test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

deploy: build up
	@echo "✅ Deployed successfully!"
	@echo "Access: http://localhost:8000"

backup-db:
	docker-compose exec db pg_dump -U postgres stj_fundamentos > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup created!"

restore-db:
	@read -p "Enter backup file name: " backup; \
	docker-compose exec -T db psql -U postgres stj_fundamentos < $$backup

generate-secret:
	@python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

setup:
	cp .env.example .env
	@echo "📝 Edit .env file with your settings"
	@echo "Then run: make deploy"
