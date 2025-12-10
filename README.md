# STJ Fundamentos Legais

Sistema de consulta de fundamentos legais do Superior Tribunal de Justiça (STJ).

## 🚀 Início Rápido

### Desenvolvimento Local

```bash
# Entrar no diretório
cd stj_fundamentos

# Instalar dependências
pip install -r requirements.txt

# Aplicar migrações
python manage.py migrate

# Importar dados (CSVs devem estar em ./data/)
python manage.py importar_fundamentos --dir=./data

# Criar superusuário (opcional)
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

### Com Docker

```bash
# Copiar arquivo de ambiente
cp .env.example .env

# Editar variáveis de ambiente
nano .env

# Iniciar com Docker Compose
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### Deploy no EasyPanel

📖 **Guia rápido:** [QUICKSTART_EASYPANEL.md](QUICKSTART_EASYPANEL.md)

📚 **Documentação completa:** [DEPLOY.md](DEPLOY.md)

## 📍 Endpoints

### Interface Web
- `/` - Página de busca
- `/arvore/` - Visualização em árvore
- `/detalhe/{seq}/` - Detalhe de um fundamento
- `/admin/` - Painel administrativo

### API REST
- `GET /api/fundamentos/` - Lista todos os fundamentos
- `GET /api/fundamentos/{seq}/` - Detalhe de um fundamento
- `GET /api/fundamentos/arvore/` - Estrutura em árvore
- `GET /api/fundamentos/busca/?q=termo` - Busca textual
- `GET /api/fundamentos/estatisticas/` - Estatísticas

### Filtros da API
- `?tipo=AFIRE` - Filtra por tipo de recurso
- `?categoria=CIVEL` - Filtra por categoria
- `?selecionavel=true` - Apenas selecionáveis
- `?raiz=true` - Apenas fundamentos raiz
- `?pai=123` - Filhos de um fundamento específico
- `?search=súmula` - Busca textual

## 📂 Estrutura dos Dados

| Tipo | Descrição |
|------|-----------|
| AFIRE | Fundamentos de Inadmissão REsp |
| AFIPO_RESP | REsp e AREsp |
| AFIPO_RMS | RMS - Recurso em Mandado de Segurança |
| AFIREQ | Requisitos de Fundamentos |

## 🔑 Credenciais Padrão

- **Admin:** admin / admin123

⚠️ **IMPORTANTE:** Altere a senha padrão em produção!

## 🐳 Docker & Deploy

Este projeto está pronto para deploy com Docker e suporta:

- ✅ Docker & Docker Compose
- ✅ EasyPanel
- ✅ PostgreSQL ou SQLite
- ✅ Nginx (configuração incluída)
- ✅ Health checks
- ✅ Arquivos estáticos otimizados (WhiteNoise)

### Arquivos de Configuração

- `Dockerfile` - Imagem Docker otimizada multi-stage
- `docker-compose.yml` - Orquestração com PostgreSQL
- `entrypoint.sh` - Script de inicialização automática
- `.env.example` - Template de variáveis de ambiente
- `nginx.conf` - Configuração Nginx (opcional)

### Variáveis de Ambiente Principais

```env
DJANGO_SECRET_KEY=sua-chave-secreta
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=seudominio.com
DB_ENGINE=postgresql
DB_NAME=stj_fundamentos
DB_USER=postgres
DB_PASSWORD=senha-segura
DB_HOST=db
DB_PORT=5432
```

## 📖 Documentação

- [DEPLOY.md](DEPLOY.md) - Guia completo de deploy
- [QUICKSTART_EASYPANEL.md](QUICKSTART_EASYPANEL.md) - Deploy rápido no EasyPanel

## 🛠️ Tecnologias

- **Backend:** Django 4.2+ & Django REST Framework
- **Frontend:** TailwindCSS, Alpine.js, HTMX
- **Database:** PostgreSQL (produção) / SQLite (dev)
- **Server:** Gunicorn
- **Static Files:** WhiteNoise

## 📊 Dados

O sistema contém **973 fundamentos legais** distribuídos em:
- AFIRE: 393 fundamentos
- AFIPO_RESP: 261 fundamentos
- AFIPO_RMS: 152 fundamentos
- AFIREQ: 167 fundamentos
