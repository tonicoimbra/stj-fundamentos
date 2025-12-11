#!/usr/bin/env python3
"""
Script para corrigir problemas de encoding nos arquivos CSV do STJ.

Problemas identificados:
- Caracteres box-drawing (┐, └, ─, etc.) sendo usados no lugar de aspas
- Padrão: ┐texto└ deveria ser "texto" ou apenas texto

Autor: Script gerado para correção de dados STJ
Data: 2025-12-10
"""

import os
import sys
import shutil
from datetime import datetime
import re
import csv


class EncodingFixer:
    """Classe para corrigir problemas de encoding em arquivos CSV."""

    def __init__(self, data_dir='./data'):
        self.data_dir = data_dir
        self.backup_suffix = '_backup'
        self.corrections_report = []

        # Dicionário de substituições para caracteres corrompidos
        self.char_replacements = {
            '┐': '"',  # Box-drawing character -> aspas
            '└': '"',  # Box-drawing character -> aspas
            '─': '-',  # Box-drawing horizontal -> hífen
            '│': '|',  # Box-drawing vertical -> pipe
            '┌': '"',  # Box-drawing corner -> aspas
            '┘': '"',  # Box-drawing corner -> aspas
            '├': '|',  # Box-drawing tee -> pipe
            '┤': '|',  # Box-drawing tee -> pipe
            '┬': '-',  # Box-drawing tee -> hífen
            '┴': '-',  # Box-drawing tee -> hífen
            '┼': '+',  # Box-drawing cross -> plus
        }

        # Arquivos a processar
        self.csv_files = [
            'AFIRE_202505141514.csv',
            'AFIPO_(REsp_e AREsp)_202505141515.csv',
            'AFIPO_(RMS)_202505141515.csv',
            'AFIREQ_202505141516.csv'
        ]

    def detect_encoding(self, file_path):
        """
        Detecta o encoding do arquivo.

        Args:
            file_path: Caminho do arquivo

        Returns:
            str: Encoding detectado
        """
        # Tentar ler com UTF-8 primeiro
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read()
            return 'utf-8'
        except UnicodeDecodeError:
            pass

        # Tentar outros encodings comuns
        encodings = ['latin-1', 'cp1252', 'iso-8859-1']
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    f.read()
                return enc
            except UnicodeDecodeError:
                continue

        return 'utf-8'  # Fallback

    def analyze_file(self, file_path):
        """
        Analisa um arquivo em busca de problemas de encoding.

        Args:
            file_path: Caminho do arquivo

        Returns:
            dict: Relatório de análise com caracteres problemáticos encontrados
        """
        encoding = self.detect_encoding(file_path)

        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            content = f.read()

        report = {
            'file': os.path.basename(file_path),
            'encoding': encoding,
            'size': len(content),
            'lines': content.count('\n') + 1,
            'problems': {}
        }

        # Procurar caracteres problemáticos
        for char, replacement in self.char_replacements.items():
            count = content.count(char)
            if count > 0:
                report['problems'][char] = {
                    'count': count,
                    'replacement': replacement,
                    'examples': []
                }

                # Encontrar exemplos de contexto
                pattern = f'.{{0,30}}{re.escape(char)}.{{0,30}}'
                matches = re.findall(pattern, content)
                report['problems'][char]['examples'] = matches[:3]

        return report

    def fix_content(self, content):
        """
        Corrige o conteúdo substituindo caracteres problemáticos.

        Args:
            content: Conteúdo do arquivo

        Returns:
            tuple: (conteúdo corrigido, número de substituições)
        """
        fixed_content = content
        total_replacements = 0

        for old_char, new_char in self.char_replacements.items():
            count = fixed_content.count(old_char)
            if count > 0:
                fixed_content = fixed_content.replace(old_char, new_char)
                total_replacements += count

        return fixed_content, total_replacements

    def create_backup(self, file_path):
        """
        Cria backup do arquivo original.

        Args:
            file_path: Caminho do arquivo

        Returns:
            str: Caminho do backup criado
        """
        backup_path = f"{file_path}{self.backup_suffix}"
        shutil.copy2(file_path, backup_path)
        return backup_path

    def process_file(self, file_path):
        """
        Processa um arquivo, corrigindo problemas de encoding.

        Args:
            file_path: Caminho do arquivo

        Returns:
            dict: Relatório do processamento
        """
        print(f"\n{'='*80}")
        print(f"Processando: {os.path.basename(file_path)}")
        print('='*80)

        # Analisar arquivo
        analysis = self.analyze_file(file_path)

        if not analysis['problems']:
            print("✓ Nenhum problema encontrado neste arquivo")
            return {
                'file': analysis['file'],
                'status': 'ok',
                'replacements': 0
            }

        # Mostrar problemas encontrados
        print(f"\nProblemas encontrados:")
        for char, info in analysis['problems'].items():
            print(f"  '{char}' → '{info['replacement']}': {info['count']} ocorrências")

        # Mostrar exemplos
        print(f"\nExemplos de contexto:")
        for char, info in analysis['problems'].items():
            if info['examples']:
                print(f"\n  Char '{char}' → '{info['replacement']}':")
                for example in info['examples'][:2]:
                    print(f"    ...{example}...")

        # Criar backup
        print(f"\nCriando backup...")
        backup_path = self.create_backup(file_path)
        print(f"  Backup criado: {os.path.basename(backup_path)}")

        # Ler conteúdo
        encoding = analysis['encoding']
        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            content = f.read()

        # Corrigir conteúdo
        print(f"\nAplicando correções...")
        fixed_content, total_replacements = self.fix_content(content)

        # Salvar arquivo corrigido
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.write(fixed_content)

        print(f"✓ Arquivo corrigido: {total_replacements} substituições realizadas")

        # Validar leitura do CSV
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter='#')
                lines = list(reader)
            print(f"✓ Validação: CSV carregado com sucesso ({len(lines)} linhas)")
        except Exception as e:
            print(f"⚠ Aviso na validação: {e}")

        return {
            'file': analysis['file'],
            'status': 'fixed',
            'replacements': total_replacements,
            'backup': os.path.basename(backup_path),
            'problems': analysis['problems']
        }

    def generate_report(self, results):
        """
        Gera relatório final das correções.

        Args:
            results: Lista de resultados do processamento

        Returns:
            str: Relatório formatado
        """
        report_lines = [
            "\n" + "="*80,
            "RELATÓRIO FINAL DE CORREÇÕES",
            "="*80,
            f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Diretório: {os.path.abspath(self.data_dir)}",
            f"Arquivos processados: {len(results)}",
            ""
        ]

        total_replacements = 0
        files_fixed = 0

        for result in results:
            report_lines.append(f"\n{'-'*80}")
            report_lines.append(f"Arquivo: {result['file']}")
            report_lines.append(f"Status: {result['status']}")
            report_lines.append(f"Substituições: {result['replacements']}")

            if result['status'] == 'fixed':
                files_fixed += 1
                total_replacements += result['replacements']
                report_lines.append(f"Backup: {result['backup']}")

                if 'problems' in result:
                    report_lines.append("\nCaracteres corrigidos:")
                    for char, info in result['problems'].items():
                        report_lines.append(
                            f"  '{char}' → '{info['replacement']}': {info['count']} ocorrências"
                        )

        report_lines.extend([
            "\n" + "="*80,
            "RESUMO",
            "="*80,
            f"Total de arquivos processados: {len(results)}",
            f"Arquivos corrigidos: {files_fixed}",
            f"Arquivos sem problemas: {len(results) - files_fixed}",
            f"Total de substituições: {total_replacements}",
            "="*80
        ])

        return "\n".join(report_lines)

    def run(self):
        """
        Executa o processo completo de correção.
        """
        print("\n" + "="*80)
        print("CORRETOR DE ENCODING - ARQUIVOS CSV STJ")
        print("="*80)
        print(f"Diretório: {os.path.abspath(self.data_dir)}")
        print(f"Arquivos a processar: {len(self.csv_files)}")

        results = []

        for csv_file in self.csv_files:
            file_path = os.path.join(self.data_dir, csv_file)

            if not os.path.exists(file_path):
                print(f"\n⚠ Arquivo não encontrado: {csv_file}")
                results.append({
                    'file': csv_file,
                    'status': 'not_found',
                    'replacements': 0
                })
                continue

            try:
                result = self.process_file(file_path)
                results.append(result)
            except Exception as e:
                print(f"\n✗ Erro ao processar {csv_file}: {e}")
                results.append({
                    'file': csv_file,
                    'status': 'error',
                    'replacements': 0,
                    'error': str(e)
                })

        # Gerar e exibir relatório
        report = self.generate_report(results)
        print(report)

        # Salvar relatório em arquivo
        report_file = os.path.join(self.data_dir, 'relatorio_correcoes.txt')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n✓ Relatório salvo em: {report_file}")

        return results


def main():
    """Função principal."""
    # Verificar se o diretório data/ existe
    data_dir = './data'

    if len(sys.argv) > 1:
        data_dir = sys.argv[1]

    if not os.path.exists(data_dir):
        print(f"✗ Erro: Diretório '{data_dir}' não encontrado")
        print(f"\nUso: {sys.argv[0]} [diretório]")
        sys.exit(1)

    # Criar e executar o corretor
    fixer = EncodingFixer(data_dir)
    results = fixer.run()

    # Retornar código de saída apropriado
    if any(r['status'] == 'error' for r in results):
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
