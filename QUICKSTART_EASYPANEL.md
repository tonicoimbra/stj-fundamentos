# 🚀 Deploy Rápido no EasyPanel

Guia rápido de 5 minutos para fazer deploy no EasyPanel.

## 1️⃣ Preparar Código

```bash
# Clone ou navegue até o projeto
cd stj_fundamentos

# Certifique-se que todos os arquivos estão commitados
git add .
git commit -m "Ready for EasyPanel deployment"
git push
```

## 2️⃣ Criar App no EasyPanel

1. Login no EasyPanel
2. **Create New App** → **From Git Repository**
3. Conecte seu repositório GitHub/GitLab
4. Branch: `main`
5. Root Directory: `/`

## 3️⃣ Configurar Variáveis de Ambiente

Copie e cole estas variáveis (ajuste os valores):

```env
DJANGO_SECRET_KEY=cole-aqui-uma-chave-gerada
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=seudominio.com,www.seudominio.com
DB_ENGINE=postgresql
DB_NAME=stj_fundamentos
DB_USER=postgres
DB_PASSWORD=sua-senha-segura
DB_HOST=db
DB_PORT=5432
```

**Gerar SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 4️⃣ Criar Database

No EasyPanel:
1. **Add Service** → **PostgreSQL**
2. Name: `stj-fundamentos-db`
3. Version: `16`
4. Copie as credenciais para as variáveis acima

## 5️⃣ Deploy

1. Clique em **Deploy**
2. Aguarde build (2-3 minutos)
3. Aplicação estará disponível!

## 6️⃣ Verificar

- Web: `https://seu-app.easypanel.host/`
- API: `https://seu-app.easypanel.host/api/fundamentos/`
- Admin: `https://seu-app.easypanel.host/admin/`

**Login padrão:** `admin` / `admin123`

⚠️ **Altere a senha imediatamente!**

## 7️⃣ Upload de Dados (Opcional)

Se os dados não foram incluídos no build:

### Via Console:
```bash
# Acessar container
docker exec -it <container-id> bash

# Upload dados (use SFTP/SCP para copiar CSVs)
python manage.py importar_fundamentos --dir=/app/data
```

### Via Volume:
1. Configure volume: `/app/data`
2. Upload CSVs via SFTP
3. Restart container

## 🎯 Checklist Pós-Deploy

- [ ] Aplicação acessível
- [ ] API retornando dados
- [ ] Admin funcionando
- [ ] Senha do admin alterada
- [ ] SSL/HTTPS ativo
- [ ] Domínio customizado configurado (se aplicável)
- [ ] Dados importados
- [ ] Backup do banco configurado

## ⚡ Comandos Úteis

```bash
# Logs
docker logs -f <container-id>

# Acessar shell Django
docker exec -it <container-id> python manage.py shell

# Criar superuser adicional
docker exec -it <container-id> python manage.py createsuperuser

# Rodar migrações
docker exec -it <container-id> python manage.py migrate

# Coletar static files
docker exec -it <container-id> python manage.py collectstatic
```

## 🆘 Problemas Comuns

### Container não inicia
- Verifique logs no EasyPanel
- Confirme variáveis de ambiente
- Verifique se PostgreSQL está rodando

### Erro 500
- `DEBUG=False` está configurado?
- `ALLOWED_HOSTS` tem seu domínio?
- Verifique logs para detalhes

### Database error
- PostgreSQL está rodando?
- Credenciais corretas?
- Host correto (`db` ou IP)?

---

**Documentação completa:** Ver `DEPLOY.md`

**Suporte:** Verifique logs e documentação do EasyPanel
