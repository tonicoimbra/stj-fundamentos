#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para corrigir problemas de codificação nos arquivos da pasta data.
O problema: arquivos UTF-8 sendo interpretados incorretamente como Latin-1.
"""

import os
import shutil
from pathlib import Path


def fix_encoding(text):
    """
    Tenta corrigir texto com problemas de codificação.
    Converte texto mal interpretado (UTF-8 lido como Latin-1) de volta ao correto.
    """
    try:
        # Tenta corrigir: encode como latin-1 (volta aos bytes originais)
        # e decode como utf-8 (interpretação correta)
        fixed_text = text.encode('latin-1').decode('utf-8')
        return fixed_text
    except (UnicodeDecodeError, UnicodeEncodeError):
        # Se não conseguir corrigir, retorna o texto original
        return text


def process_file(file_path, backup_dir):
    """
    Processa um arquivo, corrigindo sua codificação.
    """
    print(f"\nProcessando: {file_path.name}")

    # Faz backup do arquivo original
    backup_path = backup_dir / file_path.name
    shutil.copy2(file_path, backup_path)
    print(f"  Backup criado: {backup_path}")

    # Lê o arquivo original
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"  Erro ao ler arquivo: {e}")
        return False

    # Corrige a codificação
    fixed_content = fix_encoding(content)

    # Verifica se houve mudanças
    if fixed_content == content:
        print(f"  Nenhuma correção necessária")
        return False

    # Salva o arquivo corrigido
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"  Arquivo corrigido com sucesso!")
        return True
    except Exception as e:
        print(f"  Erro ao salvar arquivo corrigido: {e}")
        # Restaura o backup em caso de erro
        shutil.copy2(backup_path, file_path)
        return False


def main():
    """
    Função principal que processa todos os arquivos da pasta data.
    """
    # Define diretórios
    data_dir = Path(__file__).parent / 'data'
    backup_dir = data_dir / 'backup_original'

    # Cria diretório de backup se não existir
    backup_dir.mkdir(exist_ok=True)

    print("="*70)
    print("CORREÇÃO DE CODIFICAÇÃO - Arquivos STJ Fundamentos")
    print("="*70)
    print(f"\nDiretório de dados: {data_dir}")
    print(f"Diretório de backup: {backup_dir}")

    # Lista arquivos a processar
    files_to_process = []
    for pattern in ['*.csv', '*.txt']:
        files_to_process.extend(data_dir.glob(pattern))

    if not files_to_process:
        print("\nNenhum arquivo CSV ou TXT encontrado para processar.")
        return

    print(f"\nArquivos encontrados: {len(files_to_process)}")
    for f in files_to_process:
        print(f"  - {f.name}")

    # Processa cada arquivo
    print("\n" + "-"*70)
    print("INICIANDO PROCESSAMENTO")
    print("-"*70)

    files_fixed = 0
    for file_path in files_to_process:
        if process_file(file_path, backup_dir):
            files_fixed += 1

    # Resumo
    print("\n" + "="*70)
    print("RESUMO")
    print("="*70)
    print(f"Total de arquivos processados: {len(files_to_process)}")
    print(f"Arquivos corrigidos: {files_fixed}")
    print(f"Backups salvos em: {backup_dir}")
    print("\nConcluído!")


if __name__ == '__main__':
    main()
