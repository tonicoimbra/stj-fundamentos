#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para analisar a codificação dos arquivos e detectar o problema real.
"""

from pathlib import Path


def analyze_file(file_path):
    """
    Analisa a codificação de um arquivo.
    """
    print(f"\n{'='*70}")
    print(f"Arquivo: {file_path.name}")
    print('='*70)

    # Testa diferentes codificações
    print(f"\nTeste de leitura com diferentes codificações:")

    for encoding in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read(500)  # Lê primeiros 500 caracteres

            # Procura por padrões problemáticos
            if 'Ã§Ã£o' in content or 'legislaÃ§Ã£o' in content:
                print(f"  {encoding:12} - PROBLEMA DETECTADO (contém 'Ã§Ã£o')")
            else:
                print(f"  {encoding:12} - OK")

        except UnicodeDecodeError as e:
            print(f"  {encoding:12} - ERRO: {e}")

    # Mostra uma amostra do conteúdo
    print(f"\nAmostra do conteúdo (UTF-8):")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:5]
        for i, line in enumerate(lines, 1):
            preview = line[:100].strip()
            print(f"  Linha {i}: {preview}")
    except Exception as e:
        print(f"  Erro ao ler: {e}")


def main():
    """
    Função principal.
    """
    data_dir = Path(__file__).parent / 'data'

    print("="*70)
    print("ANÁLISE DE CODIFICAÇÃO - Arquivos STJ Fundamentos")
    print("="*70)

    # Analisa arquivo de texto primeiro
    txt_file = data_dir / 'texto_fundamentos.txt'
    if txt_file.exists():
        analyze_file(txt_file)

    # Analisa um dos CSVs
    csv_file = data_dir / 'AFIRE_202505141514.csv'
    if csv_file.exists():
        analyze_file(csv_file)


if __name__ == '__main__':
    main()
