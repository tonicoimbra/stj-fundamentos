#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para converter o arquivo texto_fundamentos.txt de Latin-1 para UTF-8.
"""

import shutil
from pathlib import Path


def convert_file():
    """
    Converte o arquivo texto_fundamentos.txt de Latin-1 para UTF-8.
    """
    # Define caminhos
    data_dir = Path(__file__).parent / 'data'
    txt_file = data_dir / 'texto_fundamentos.txt'
    backup_dir = data_dir / 'backup_original'

    if not txt_file.exists():
        print(f"Erro: Arquivo não encontrado: {txt_file}")
        return False

    print("="*70)
    print("CONVERSÃO DE CODIFICAÇÃO - texto_fundamentos.txt")
    print("="*70)

    # Cria diretório de backup se não existir
    backup_dir.mkdir(exist_ok=True)

    # Faz backup
    backup_path = backup_dir / 'texto_fundamentos_latin1.txt'
    shutil.copy2(txt_file, backup_path)
    print(f"\nBackup criado: {backup_path}")

    # Lê o arquivo em Latin-1
    print(f"\nLendo arquivo em Latin-1...")
    try:
        with open(txt_file, 'r', encoding='latin-1') as f:
            content = f.read()
        print(f"  Sucesso! {len(content)} caracteres lidos")
    except Exception as e:
        print(f"  Erro ao ler: {e}")
        return False

    # Mostra uma amostra antes da conversão
    print(f"\nAmostra ANTES da conversão:")
    lines = content.split('\n')[:3]
    for i, line in enumerate(lines, 1):
        preview = line[:80]
        print(f"  Linha {i}: {preview}")

    # Salva o arquivo em UTF-8
    print(f"\nSalvando arquivo em UTF-8...")
    try:
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Sucesso! Arquivo salvo")
    except Exception as e:
        print(f"  Erro ao salvar: {e}")
        # Restaura backup em caso de erro
        shutil.copy2(backup_path, txt_file)
        return False

    # Verifica o resultado
    print(f"\nVerificando resultado...")
    try:
        with open(txt_file, 'r', encoding='utf-8') as f:
            content_check = f.read()

        # Mostra uma amostra depois da conversão
        print(f"\nAmostra DEPOIS da conversão:")
        lines = content_check.split('\n')[:3]
        for i, line in enumerate(lines, 1):
            preview = line[:80]
            print(f"  Linha {i}: {preview}")

        # Verifica se ainda há problemas
        if 'Ã§Ã£o' in content_check or 'legislaÃ§Ã£o' in content_check:
            print(f"\n⚠ AVISO: Ainda há problemas de codificação detectados!")
            return False
        else:
            print(f"\n✓ Sucesso! Arquivo convertido corretamente")
            print(f"  'legislação' agora aparece corretamente")
            return True

    except Exception as e:
        print(f"  Erro ao verificar: {e}")
        return False


def main():
    """
    Função principal.
    """
    if convert_file():
        print("\n" + "="*70)
        print("CONCLUÍDO COM SUCESSO!")
        print("="*70)
        print("\nPróximos passos:")
        print("1. Verifique manualmente o arquivo se desejar")
        print("2. Execute: python manage.py importar_fundamentos --dir=./data --clear")
        print("   para reimportar os dados com a codificação correta")
    else:
        print("\n" + "="*70)
        print("ERRO NA CONVERSÃO")
        print("="*70)


if __name__ == '__main__':
    main()
