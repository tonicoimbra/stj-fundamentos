#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para corrigir problemas de codificação usando mapeamento direto.
Corrige caracteres UTF-8 mal interpretados como Latin-1.
"""

import shutil
from pathlib import Path


# Mapeamento de caracteres problemáticos para os corretos
CHAR_MAP = {
    # Combinações complexas (processar primeiro)
    'Ã§Ã£o': 'ção',
    'Ã§Ã£': 'çã',
    'Ã§Ãµ': 'çõ',
    'REGIÃ\xa0O': 'REGIÃO',  # Ã + non-breaking space + O
    'REGIÃ O': 'REGIÃO',
    'REGIÃ£O': 'REGIÃO',
    # Caracteres acentuados minúsculos
    'Ã¡': 'á',
    'Ã©': 'é',
    'Ã­': 'í',
    'Ã³': 'ó',
    'Ãº': 'ú',
    'Ã¢': 'â',
    'Ãª': 'ê',
    'Ã´': 'ô',
    'Ã£': 'ã',
    'Ãµ': 'õ',
    'Ã§': 'ç',
    'Ã ': 'à',
    # Caracteres acentuados maiúsculos
    'Ã‡': 'Ç',
    'Ã': 'Á',
    'Ã‰': 'É',
    'Ã': 'Í',
    'Ã"': 'Ó',
    'Ãš': 'Ú',
    'Ã‚': 'Â',
    'ÃŠ': 'Ê',
    'Ã"': 'Ô',
    'Ã': 'Ã',
    'Ã•': 'Õ',
    # Casos especiais que aparecem no texto
    'Ã\xa0': 'à',  # à + non-breaking space
    'Ã ': 'à',  # à com espaço depois
    # Caracteres com espaço não-quebrável
    '\xa0': ' ',  # Non-breaking space para espaço normal (se isolado)
}


def fix_text(text):
    """
    Corrige o texto usando o mapeamento de caracteres.
    """
    fixed = text
    replacements_made = 0

    # Aplica as substituições do mais longo para o mais curto
    # para evitar substituições parciais incorretas
    for wrong, correct in sorted(CHAR_MAP.items(), key=lambda x: len(x[0]), reverse=True):
        count = fixed.count(wrong)
        if count > 0:
            fixed = fixed.replace(wrong, correct)
            replacements_made += count

    return fixed, replacements_made


def process_file(file_path):
    """
    Processa um arquivo, corrigindo caracteres problemáticos.
    """
    print(f"\n{'='*70}")
    print(f"Processando: {file_path.name}")
    print('='*70)

    # Cria backup
    backup_dir = file_path.parent / 'backup_original'
    backup_dir.mkdir(exist_ok=True)
    backup_path = backup_dir / f"{file_path.stem}_before_fix{file_path.suffix}"

    if not backup_path.exists():
        shutil.copy2(file_path, backup_path)
        print(f"Backup criado: {backup_path}")
    else:
        print(f"Backup já existe: {backup_path}")

    # Lê o arquivo
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        print(f"Arquivo lido: {len(content)} caracteres")
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return False

    # Mostra amostra antes
    print(f"\nAmostra ANTES:")
    lines = content.split('\n')
    for i in [1, 2]:  # Linhas 2 e 3 (índice 1 e 2)
        if i < len(lines):
            preview = lines[i][:100]
            print(f"  Linha {i+1}: {preview}")

    # Corrige o conteúdo
    fixed_content, replacements = fix_text(content)

    if replacements == 0:
        print(f"\nNenhuma correção necessária")
        return False

    print(f"\nCorreções realizadas: {replacements} substituições")

    # Mostra amostra depois
    print(f"\nAmostra DEPOIS:")
    lines_fixed = fixed_content.split('\n')
    for i in [1, 2]:
        if i < len(lines_fixed):
            preview = lines_fixed[i][:100]
            print(f"  Linha {i+1}: {preview}")

    # Salva o arquivo corrigido
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"\nArquivo salvo com sucesso!")
        return True
    except Exception as e:
        print(f"\nErro ao salvar: {e}")
        # Restaura backup
        shutil.copy2(backup_path, file_path)
        return False


def main():
    """
    Função principal.
    """
    data_dir = Path(__file__).parent / 'data'

    print("="*70)
    print("CORREÇÃO DE CODIFICAÇÃO - Mapeamento Direto")
    print("="*70)

    # Lista todos os arquivos CSV e TXT
    files_to_process = []
    for pattern in ['*.csv', '*.txt']:
        files_to_process.extend(data_dir.glob(pattern))

    if not files_to_process:
        print("\nNenhum arquivo encontrado")
        return

    print(f"\nArquivos encontrados: {len(files_to_process)}")

    # Processa cada arquivo
    files_fixed = 0
    for file_path in files_to_process:
        if process_file(file_path):
            files_fixed += 1

    # Resumo
    print(f"\n{'='*70}")
    print("RESUMO")
    print('='*70)
    print(f"Arquivos processados: {len(files_to_process)}")
    print(f"Arquivos corrigidos: {files_fixed}")

    if files_fixed > 0:
        print(f"\nPróximos passos:")
        print(f"1. Verifique os arquivos corrigidos")
        print(f"2. Execute: python manage.py importar_fundamentos --dir=./data --clear")


if __name__ == '__main__':
    main()
