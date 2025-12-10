# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django-based REST API and web interface for querying legal fundamentos from Brazil's Superior Tribunal de Justiça (STJ). The system manages 973 hierarchical legal fundamentos across 4 types of resources with a self-referential parent-child tree structure.

## Commands

### Development

```bash
# Install dependencies
pip install -r requirements.txt

# Database setup
python manage.py migrate

# Import fundamentos from CSV files (data/ directory)
python manage.py importar_fundamentos --dir=./data

# Import with clean slate
python manage.py importar_fundamentos --dir=./data --clear

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Collect static files (production)
python manage.py collectstatic --no-input
```

### Docker

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f web

# Run migrations in container
docker-compose exec web python manage.py migrate

# Import data in container
docker-compose exec web python manage.py importar_fundamentos --dir=/app/data
```

### Testing

```bash
# Run tests
python manage.py test fundamentos
```

## Architecture

### Data Model

The core is a self-referential hierarchy in `fundamentos/models.py`:

- **FundamentoLegal**: Main model with self-referencing `pai` (parent) ForeignKey creating tree structure
  - Key methods: `nivel` (depth in tree), `caminho` (path to root), `get_descendentes()` (all children recursively)
  - Boolean flags: `neutro`, `informacao`, `justificativa`, `selecionavel` (AFIRE-specific)
  - Enum fields: `tipo_recurso` (4 types: AFIRE, AFIPO_RESP, AFIPO_RMS, AFIREQ), `categoria` (CIVEL/CRIMINAL/GERAL)

- **TextoFundamento**: Related HTML texts and legislation references

### API Architecture

REST API built with Django REST Framework in `fundamentos/views.py`:

- **FundamentoLegalViewSet**: Read-only viewset with custom actions
  - Standard CRUD via `/api/fundamentos/`
  - Custom actions: `/arvore/`, `/busca/`, `/estatisticas/`, `/{seq}/descendentes/`
  - Query filters: `?tipo=`, `?categoria=`, `?selecionavel=`, `?raiz=true`, `?pai={seq}`
  - Search with `?search=` (DRF) or `?q=` (custom busca action)

- **Serializers** (`serializers.py`):
  - `FundamentoLegalListSerializer`: Compact for listings
  - `FundamentoLegalDetailSerializer`: Full detail with nested relationships
  - `FundamentoLegalTreeSerializer`: Recursive tree structure

### URL Structure

Defined in `fundamentos/urls.py`:
- `/` - Web search interface
- `/arvore/` - Tree visualization
- `/detalhe/{seq}/` - Detail view
- `/admin/` - Django admin
- `/api/fundamentos/` - REST API (DRF router)

### Data Import

Custom management command in `fundamentos/management/commands/importar_fundamentos.py`:

1. Reads CSV files from data/ using pandas (sep='#')
2. Creates FundamentoLegal instances in transaction
3. Two-pass approach: first creates all fundamentos, then updates parent relationships
4. Imports optional TextoFundamento from texto_fundamentos.txt
5. Validates and fixes hierarchy after import

CSV format expectations:
- SEQ_FUNDAMENTO_LEGAL: Primary key
- SEQ_FUNDAMENTO_LEGAL_PAI: Parent reference
- DESCRICAO, GLOSSARIO: Text fields
- NEUTRO, INFORMACAO, JUSTIFICATIVA, SELECIONAVEL: Boolean flags (S/N)

### Settings

`config/settings.py` uses environment variables:
- Dual database support: PostgreSQL (production) or SQLite (dev) via `DB_ENGINE`
- WhiteNoise for static files in production
- Security hardening enabled when `DEBUG=False`
- SECURE_PROXY_SSL_HEADER configured for reverse proxy (EasyPanel/Nginx)

### Frontend

Templates in `fundamentos/templates/fundamentos/`:
- TailwindCSS for styling
- Alpine.js for interactivity
- HTMX for dynamic content loading

## Key Patterns

### Working with Hierarchy

When querying or displaying fundamentos, be aware of the tree structure:

```python
# Get root nodes
raizes = FundamentoLegal.objects.filter(pai__isnull=True)

# Get children
filhos = fundamento.filhos.all()

# Get full ancestry path
caminho = fundamento.caminho

# Get all descendants recursively
descendentes = fundamento.get_descendentes()
```

### Database Configuration

The app detects database type via `DB_ENGINE` environment variable:
- `postgresql`: Uses psycopg2-binary with full DB credentials
- `sqlite3` (default): Uses local db.sqlite3 file

### Static Files

In production, WhiteNoise serves static files. Always run `collectstatic` before deployment. Static files are served from `/static/` and stored in `staticfiles/` directory.

## Data Context

**4 Resource Types:**
- AFIRE: Fundamentos de Inadmissão REsp (393 items)
- AFIPO_RESP: REsp e AREsp (261 items)
- AFIPO_RMS: RMS - Recurso em Mandado de Segurança (152 items)
- AFIREQ: Requisitos de Fundamentos (167 items)

**CSV Files in data/:**
- AFIRE_202505141514.csv
- AFIPO_REsp_e_AREsp_202505141515.csv
- AFIPO_RMS_202505141515.csv
- AFIREQ_202505141516.csv
- texto_fundamentos.txt (optional HTML texts)

## Deployment

Docker-ready with multi-stage Dockerfile and docker-compose.yml:
- Gunicorn WSGI server (4 workers)
- PostgreSQL 16 with health checks
- Automatic migrations via entrypoint.sh
- Health check endpoint: `/api/fundamentos/`

Required environment variables for production:
- DJANGO_SECRET_KEY
- DJANGO_DEBUG=False
- DJANGO_ALLOWED_HOSTS
- DB_ENGINE=postgresql
- DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
