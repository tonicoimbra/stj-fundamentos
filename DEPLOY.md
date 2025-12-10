# Deploy STJ Fundamentos no EasyPanel

Guia completo para fazer deploy da aplicação STJ Fundamentos Legais no EasyPanel.

## 📋 Pré-requisitos

- Acesso ao EasyPanel na sua VPS
- Repositório Git (GitHub, GitLab, etc.)
- Domínio configurado (opcional, mas recomendado)

## 🚀 Passo a Passo

### 1. Preparar o Repositório Git

```bash
# Inicializar git (se ainda não foi feito)
git init

# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "Preparado para deploy no EasyPanel"

# Adicionar repositório remoto
git remote add origin https://github.com/seu-usuario/stj-fundamentos.git

# Push para o repositório
git push -u origin main
```

### 2. Criar Aplicação no EasyPanel

1. Acesse seu painel EasyPanel
2. Clique em **"Create New App"**
3. Escolha **"From Git"**
4. Conecte seu repositório
5. Selecione a branch **main**

### 3. Configurar Variáveis de Ambiente

No painel do EasyPanel, configure as seguintes variáveis:

#### Obrigatórias:
```env
DJANGO_SECRET_KEY=sua-chave-secreta-aqui-gere-uma-nova
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=seudominio.com,www.seudominio.com
```

#### Database (PostgreSQL):
```env
DB_ENGINE=postgresql
DB_NAME=stj_fundamentos
DB_USER=postgres
DB_PASSWORD=senha-segura-do-banco
DB_HOST=db
DB_PORT=5432
```

**💡 Dica:** Para gerar uma SECRET_KEY segura:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Configurar Banco de Dados

**Opção A: Usar PostgreSQL do EasyPanel (Recomendado)**

1. No EasyPanel, crie um serviço PostgreSQL
2. Copie as credenciais e use nas variáveis de ambiente acima

**Opção B: Usar SQLite (Apenas para testes)**

```env
DB_ENGINE=sqlite3
# Não precisa configurar outras variáveis DB_*
```

### 5. Configurar Porta

O EasyPanel geralmente espera a aplicação na porta **8000** (já configurado).

### 6. Build & Deploy

1. No painel do EasyPanel, clique em **"Deploy"**
2. Aguarde o build do Docker
3. A aplicação será iniciada automaticamente

### 7. Verificar Deploy

Acesse os seguintes endpoints para verificar:

- **Interface Web:** `https://seudominio.com/`
- **API:** `https://seudominio.com/api/fundamentos/`
- **Admin:** `https://seudominio.com/admin/`

**Credenciais padrão do admin:**
- Usuário: `admin`
- Senha: `admin123`

⚠️ **IMPORTANTE:** Altere a senha padrão imediatamente após o primeiro acesso!

## 📁 Upload de Dados

### Opção 1: Via Volume do EasyPanel

1. Configure um volume no EasyPanel apontando para `/app/data`
2. Faça upload dos arquivos CSV:
   - `AFIRE_202505141514.csv`
   - `AFIPO_REsp_e_AREsp_202505141515.csv`
   - `AFIPO_RMS_202505141515.csv`
   - `AFIREQ_202505141516.csv`
   - `texto_fundamentos.txt`

### Opção 2: Via Console do Container

```bash
# Acessar o container
docker exec -it <container-name> bash

# Criar diretório
mkdir -p /app/data

# Importar dados
python manage.py importar_fundamentos --dir=/app/data
```

### Opção 3: Incluir no Build

Coloque os arquivos CSV na pasta `data/` antes do build. Eles serão copiados automaticamente.

## 🔧 Configurações Adicionais

### SSL/HTTPS

O EasyPanel geralmente configura SSL automaticamente. Certifique-se de:
- ✅ Domínio apontando para o servidor
- ✅ Certificado SSL ativo no EasyPanel

### Domínio Customizado

1. No EasyPanel, vá em **"Domains"**
2. Adicione seu domínio
3. Atualize `DJANGO_ALLOWED_HOSTS` com seu domínio
4. Reconfigure a aplicação

### Backup do Banco de Dados

**PostgreSQL:**
```bash
# Backup
docker exec <postgres-container> pg_dump -U postgres stj_fundamentos > backup.sql

# Restore
docker exec -i <postgres-container> psql -U postgres stj_fundamentos < backup.sql
```

**SQLite:**
```bash
# Copiar arquivo do container
docker cp <container-name>:/app/db.sqlite3 ./backup.db
```

## 🐛 Troubleshooting

### Erro: "DisallowedHost"
- Verifique `DJANGO_ALLOWED_HOSTS` nas variáveis de ambiente
- Adicione todos os domínios separados por vírgula

### Erro: "Database connection failed"
- Verifique se o serviço PostgreSQL está rodando
- Confirme as credenciais do banco
- Verifique `DB_HOST` (geralmente é `db` ou IP do serviço)

### Erro: "Static files not found"
- Execute: `python manage.py collectstatic`
- Verifique se WhiteNoise está configurado

### Container não inicia
- Verifique os logs no EasyPanel
- Confirme que todas as variáveis de ambiente estão configuradas
- Verifique se o `entrypoint.sh` tem permissão de execução

## 📊 Monitoramento

### Logs da Aplicação

No EasyPanel:
1. Acesse sua aplicação
2. Clique em **"Logs"**
3. Monitore em tempo real

### Health Check

A aplicação tem health check configurado:
```
GET /api/fundamentos/
```

Deve retornar status 200 se tudo estiver OK.

## 🔄 Atualizações

Para atualizar a aplicação:

1. Faça commit das mudanças no Git
2. Push para o repositório
3. No EasyPanel, clique em **"Redeploy"**

## 🔐 Segurança

- ✅ Gere uma nova `DJANGO_SECRET_KEY`
- ✅ Use senhas fortes para banco de dados
- ✅ Altere senha padrão do admin
- ✅ Configure `DEBUG=False` em produção
- ✅ Use HTTPS (SSL)
- ✅ Configure ALLOWED_HOSTS corretamente

## 📞 Suporte

Em caso de problemas:
1. Verifique os logs da aplicação
2. Confira as variáveis de ambiente
3. Consulte a documentação do EasyPanel
4. Revise este guia

---

## 🎉 Pronto!

Sua aplicação STJ Fundamentos está agora rodando no EasyPanel!

Acesse: `https://seudominio.com`
