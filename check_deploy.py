#!/usr/bin/env python3
"""
Pre-deployment checklist script
Verifica se o projeto está pronto para deploy
"""

import os
import sys
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def check(condition, message):
    """Print check result"""
    if condition:
        print(f"{Colors.GREEN}✓{Colors.END} {message}")
        return True
    else:
        print(f"{Colors.RED}✗{Colors.END} {message}")
        return False

def warning(message):
    """Print warning"""
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

def info(message):
    """Print info"""
    print(f"{Colors.BLUE}ℹ{Colors.END} {message}")

def main():
    print(f"\n{Colors.BLUE}{'='*60}")
    print("STJ Fundamentos - Checklist de Deploy")
    print(f"{'='*60}{Colors.END}\n")

    all_good = True

    # Check required files
    print(f"{Colors.BLUE}📁 Arquivos Necessários:{Colors.END}")
    files_to_check = [
        'Dockerfile',
        'docker-compose.yml',
        'requirements.txt',
        'entrypoint.sh',
        '.env.example',
        'manage.py',
    ]

    for file in files_to_check:
        exists = Path(file).exists()
        all_good &= check(exists, f"{file}")

    # Check .env file
    print(f"\n{Colors.BLUE}🔐 Configuração:{Colors.END}")
    env_exists = Path('.env').exists()
    if env_exists:
        warning(".env encontrado (não commitar!)")
    else:
        info(".env não encontrado (use .env.example)")

    # Check .gitignore
    gitignore_exists = Path('.gitignore').exists()
    all_good &= check(gitignore_exists, ".gitignore configurado")

    # Check data directory
    print(f"\n{Colors.BLUE}📊 Dados:{Colors.END}")
    data_dir = Path('data')
    data_exists = data_dir.exists()
    check(data_exists, "Diretório data/ existe")

    if data_exists:
        csv_files = list(data_dir.glob('*.csv'))
        check(len(csv_files) > 0, f"{len(csv_files)} arquivos CSV encontrados")

    # Security checks
    print(f"\n{Colors.BLUE}🔒 Segurança:{Colors.END}")

    # Check if SECRET_KEY is in settings
    try:
        with open('config/settings.py', 'r') as f:
            content = f.read()
            has_env_secret = 'os.getenv' in content and 'SECRET_KEY' in content
            check(has_env_secret, "SECRET_KEY usando variável de ambiente")

            has_debug_env = 'os.getenv' in content and 'DEBUG' in content
            check(has_debug_env, "DEBUG usando variável de ambiente")

            has_allowed_hosts_env = 'os.getenv' in content and 'ALLOWED_HOSTS' in content
            check(has_allowed_hosts_env, "ALLOWED_HOSTS usando variável de ambiente")
    except FileNotFoundError:
        all_good &= check(False, "config/settings.py não encontrado")

    # Check requirements
    print(f"\n{Colors.BLUE}📦 Dependências:{Colors.END}")
    try:
        with open('requirements.txt', 'r') as f:
            reqs = f.read()
            check('gunicorn' in reqs, "Gunicorn instalado")
            check('psycopg2' in reqs, "PostgreSQL driver instalado")
            check('whitenoise' in reqs, "WhiteNoise instalado")
            check('python-dotenv' in reqs, "python-dotenv instalado")
    except FileNotFoundError:
        all_good &= check(False, "requirements.txt não encontrado")

    # Recommendations
    print(f"\n{Colors.BLUE}💡 Recomendações para Deploy:{Colors.END}")
    info("1. Gere uma nova SECRET_KEY: make generate-secret")
    info("2. Configure variáveis de ambiente no EasyPanel")
    info("3. Use PostgreSQL em produção (não SQLite)")
    info("4. Configure DEBUG=False")
    info("5. Configure ALLOWED_HOSTS com seu domínio")
    info("6. Altere senha padrão do admin após deploy")
    info("7. Configure backups automáticos do banco")
    info("8. Ative SSL/HTTPS no EasyPanel")

    # Final result
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    if all_good:
        print(f"{Colors.GREEN}✅ Projeto pronto para deploy!{Colors.END}")
        return 0
    else:
        print(f"{Colors.RED}❌ Corrija os problemas acima antes do deploy{Colors.END}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
