#!/usr/bin/env python3
"""
Script para validar as correções feitas nos arquivos CSV.

Verifica:
- Integridade dos arquivos CSV
- Ausência de caracteres problemáticos
- Comparação com backups
- Estatísticas de conteúdo

Autor: Script gerado para validação STJ
Data: 2025-12-10
"""

import os
import sys
import csv
import re
from collections import Counter


class ValidationReport:
    """Classe para validar correções em arquivos CSV."""

    def __init__(self, data_dir='./data'):
        self.data_dir = data_dir

        # Caracteres que NÃO devem estar presentes após correção
        self.forbidden_chars = ['┐', '└', '─', '│', '┌', '┘', '├', '┤', '┬', '┴', '┼']

        # Arquivos para validar
        self.csv_files = [
            'AFIRE_202505141514.csv',
            'AFIPO_(REsp_e AREsp)_202505141515.csv',
            'AFIPO_(RMS)_202505141515.csv',
            'AFIREQ_202505141516.csv'
        ]

    def check_forbidden_chars(self, file_path):
        """
        Verifica se existem caracteres proibidos no arquivo.

        Args:
            file_path: Caminho do arquivo

        Returns:
            dict: Relatório de caracteres proibidos encontrados
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        forbidden_found = {}
        for char in self.forbidden_chars:
            count = content.count(char)
            if count > 0:
                forbidden_found[char] = count

        return forbidden_found

    def validate_csv_structure(self, file_path):
        """
        Valida a estrutura do CSV.

        Args:
            file_path: Caminho do arquivo

        Returns:
            dict: Estatísticas do CSV
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter='#')
                rows = list(reader)

            if not rows:
                return {'valid': False, 'error': 'Arquivo vazio'}

            # Analisar estrutura
            header = rows[0]
            num_columns = len(header)
            num_rows = len(rows) - 1  # Sem contar o cabeçalho

            # Verificar consistência de colunas
            inconsistent_rows = []
            for i, row in enumerate(rows[1:], start=1):
                if len(row) != num_columns:
                    inconsistent_rows.append((i, len(row)))

            return {
                'valid': True,
                'header': header,
                'num_columns': num_columns,
                'num_rows': num_rows,
                'inconsistent_rows': inconsistent_rows
            }

        except Exception as e:
            return {'valid': False, 'error': str(e)}

    def analyze_content(self, file_path):
        """
        Analisa o conteúdo do arquivo.

        Args:
            file_path: Caminho do arquivo

        Returns:
            dict: Estatísticas de conteúdo
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        stats = {
            'size_bytes': len(content.encode('utf-8')),
            'num_lines': content.count('\n') + 1,
            'num_chars': len(content),
            'num_acentos': len(re.findall(r'[áàâãéêíóôõúüç]', content, re.IGNORECASE)),
            'num_aspas_duplas': content.count('"'),
            'num_aspas_simples': content.count("'"),
        }

        return stats

    def compare_with_backup(self, file_path):
        """
        Compara arquivo com seu backup.

        Args:
            file_path: Caminho do arquivo

        Returns:
            dict: Resultado da comparação
        """
        backup_path = f"{file_path}_backup"

        if not os.path.exists(backup_path):
            return {'has_backup': False}

        with open(file_path, 'r', encoding='utf-8') as f:
            current_content = f.read()

        with open(backup_path, 'r', encoding='utf-8') as f:
            backup_content = f.read()

        # Contar diferenças
        diff_chars = sum(1 for c1, c2 in zip(current_content, backup_content) if c1 != c2)

        # Procurar caracteres problemáticos no backup
        backup_problems = {}
        for char in self.forbidden_chars:
            count = backup_content.count(char)
            if count > 0:
                backup_problems[char] = count

        return {
            'has_backup': True,
            'same_length': len(current_content) == len(backup_content),
            'diff_chars': diff_chars,
            'backup_problems': backup_problems
        }

    def validate_file(self, file_path):
        """
        Valida completamente um arquivo.

        Args:
            file_path: Caminho do arquivo

        Returns:
            dict: Relatório completo de validação
        """
        filename = os.path.basename(file_path)

        print(f"\n{'='*80}")
        print(f"Validando: {filename}")
        print('='*80)

        # Verificar caracteres proibidos
        print("\n1. Verificando caracteres proibidos...")
        forbidden = self.check_forbidden_chars(file_path)

        if forbidden:
            print(f"  ✗ ERRO: Caracteres proibidos encontrados:")
            for char, count in forbidden.items():
                print(f"    '{char}': {count} ocorrências")
            forbidden_status = 'FAIL'
        else:
            print(f"  ✓ OK: Nenhum caractere proibido encontrado")
            forbidden_status = 'PASS'

        # Validar estrutura CSV
        print("\n2. Validando estrutura CSV...")
        csv_validation = self.validate_csv_structure(file_path)

        if csv_validation['valid']:
            print(f"  ✓ CSV válido")
            print(f"    Colunas: {csv_validation['num_columns']}")
            print(f"    Linhas de dados: {csv_validation['num_rows']}")

            if csv_validation['inconsistent_rows']:
                print(f"  ⚠ Linhas com número inconsistente de colunas: {len(csv_validation['inconsistent_rows'])}")
                csv_status = 'WARN'
            else:
                print(f"  ✓ Todas as linhas consistentes")
                csv_status = 'PASS'
        else:
            print(f"  ✗ ERRO: {csv_validation['error']}")
            csv_status = 'FAIL'

        # Analisar conteúdo
        print("\n3. Análise de conteúdo...")
        content_stats = self.analyze_content(file_path)
        print(f"  Tamanho: {content_stats['size_bytes']:,} bytes")
        print(f"  Linhas: {content_stats['num_lines']:,}")
        print(f"  Caracteres acentuados: {content_stats['num_acentos']:,}")
        print(f"  Aspas duplas: {content_stats['num_aspas_duplas']:,}")

        # Comparar com backup
        print("\n4. Comparação com backup...")
        backup_comparison = self.compare_with_backup(file_path)

        if backup_comparison['has_backup']:
            print(f"  ✓ Backup encontrado")
            print(f"  Caracteres diferentes: {backup_comparison['diff_chars']:,}")

            if backup_comparison['backup_problems']:
                print(f"  Caracteres corrigidos no backup:")
                for char, count in backup_comparison['backup_problems'].items():
                    print(f"    '{char}': {count} ocorrências")
        else:
            print(f"  - Sem backup (arquivo não foi modificado)")

        # Status final
        print(f"\n{'='*80}")
        overall_status = 'PASS' if forbidden_status == 'PASS' and csv_status in ['PASS', 'WARN'] else 'FAIL'
        status_symbol = '✓' if overall_status == 'PASS' else '✗'
        print(f"{status_symbol} Status: {overall_status}")
        print('='*80)

        return {
            'file': filename,
            'forbidden_chars': forbidden,
            'forbidden_status': forbidden_status,
            'csv_validation': csv_validation,
            'csv_status': csv_status,
            'content_stats': content_stats,
            'backup_comparison': backup_comparison,
            'overall_status': overall_status
        }

    def run(self):
        """
        Executa validação completa de todos os arquivos.
        """
        print("\n" + "="*80)
        print("VALIDAÇÃO DE CORREÇÕES - ARQUIVOS CSV STJ")
        print("="*80)
        print(f"Diretório: {os.path.abspath(self.data_dir)}")

        results = []

        for csv_file in self.csv_files:
            file_path = os.path.join(self.data_dir, csv_file)

            if not os.path.exists(file_path):
                print(f"\n⚠ Arquivo não encontrado: {csv_file}")
                continue

            result = self.validate_file(file_path)
            results.append(result)

        # Resumo final
        print("\n" + "="*80)
        print("RESUMO FINAL")
        print("="*80)

        total = len(results)
        passed = sum(1 for r in results if r['overall_status'] == 'PASS')
        failed = sum(1 for r in results if r['overall_status'] == 'FAIL')

        print(f"\nTotal de arquivos validados: {total}")
        print(f"Aprovados (PASS): {passed}")
        print(f"Reprovados (FAIL): {failed}")

        if failed == 0:
            print("\n✓ Todas as validações passaram com sucesso!")
        else:
            print(f"\n✗ {failed} arquivo(s) com problemas")

        print("="*80)

        return results


def main():
    """Função principal."""
    data_dir = './data'

    if len(sys.argv) > 1:
        data_dir = sys.argv[1]

    if not os.path.exists(data_dir):
        print(f"✗ Erro: Diretório '{data_dir}' não encontrado")
        sys.exit(1)

    validator = ValidationReport(data_dir)
    results = validator.run()

    # Retornar código de saída
    if any(r['overall_status'] == 'FAIL' for r in results):
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
