# Repository Guidelines

This guide keeps contributions consistent for the STJ Fundamentos Legais project.

## Project Structure & Module Organization
- `config/`: Django project settings, URL routing, and ASGI/WSGI entrypoints.
- `fundamentos/`: Core app with models, serializers, views, URLs, templates, and custom management commands (e.g., data import).
- `data/`: CSV inputs for `importar_fundamentos`; keep large datasets out of version control.
- Tooling & ops: `Dockerfile`, `docker-compose.yml`, `nginx.conf`, `entrypoint.sh`, `start.sh`, `Makefile`, and `.env.example` for environment hints.
- `manage.py`: CLI entry to run migrations, server, tests, and imports.

## Build, Test, and Development Commands
- Install deps: `pip install -r requirements.txt`.
- Migrations: `python manage.py migrate`.
- Import dataset: `python manage.py importar_fundamentos --dir=./data`.
- Local server: `python manage.py runserver` or `make dev`.
- Tests: `python manage.py test` or `make test`.
- Dockerized stack: `docker-compose up -d`; common helpers via `make build|up|down|logs|shell|collectstatic|clean`.

## Coding Style & Naming Conventions
- Python: follow PEP 8 (4-space indent, `snake_case` for functions/variables, `PascalCase` for classes, module filenames in `snake_case`).
- Django/DRF: serializers as `*Serializer`, views in `views.py`, URLs in `urls.py`; favor class-based views where practical.
- Templates live under `fundamentos/templates/`; keep HTML components small and re-usable.
- Keep imports ordered (stdlib, third-party, local) and avoid unused code; prefer explicit settings in `config/settings.py` over ad-hoc constants.

## Testing Guidelines
- Use Django’s `TestCase` in `fundamentos/tests.py` or a `fundamentos/tests/` package; name files and methods `test_*`.
- Cover API endpoints, search filters, and management commands (especially data import edge cases).
- When touching migrations or data loading, add a regression test that seeds minimal fixtures and asserts expected counts/fields.
- Run `python manage.py test fundamentos` before pushing; aim to keep tests isolated from real data by mocking file reads when possible.

## Commit & Pull Request Guidelines
- Commit messages observed here are short and imperative (e.g., “Fix entrypoint.sh permissions”); keep them focused and bilingual (pt/en) if helpful.
- Each PR should describe scope, manual test steps, affected endpoints/UI, and reference issues when available.
- Include screenshots or cURL examples for visible/API changes; call out migrations, new environment variables, or data import requirements in the description.

## Security & Configuration Tips
- Never commit secrets; derive `.env` from `.env.example` and use `generate-secret` in the Makefile if needed.
- Keep `DJANGO_DEBUG=False` and `DJANGO_ALLOWED_HOSTS` set for non-local deployments; ensure static files are collected via `make collectstatic` in production flows.
