import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from fundamentos.models import FundamentoLegal, TextoFundamento, TipoRecurso, Categoria


class Command(BaseCommand):
    help = 'Importa fundamentos legais dos arquivos CSV do STJ'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dir',
            type=str,
            default='./data',
            help='Diretório com os arquivos CSV'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpar dados existentes antes de importar'
        )

    def handle(self, *args, **options):
        data_dir = options['dir']
        
        if options['clear']:
            self.stdout.write('Limpando dados existentes...')
            TextoFundamento.objects.all().delete()
            FundamentoLegal.objects.all().delete()

        # Mapeamento de arquivos para tipos de recurso
        arquivos = {
            'AFIRE': 'AFIRE_202505141514.csv',
            'AFIPO_RESP': 'AFIPO_(REsp_e AREsp)_202505141515.csv',
            'AFIPO_RMS': 'AFIPO_(RMS)_202505141515.csv',
            'AFIREQ': 'AFIREQ_202505141516.csv',
        }

        for tipo, arquivo in arquivos.items():
            filepath = os.path.join(data_dir, arquivo)
            if os.path.exists(filepath):
                self.stdout.write(f'Importando {arquivo}...')
                self.importar_csv(filepath, tipo)
            else:
                self.stdout.write(self.style.WARNING(f'Arquivo não encontrado: {filepath}'))

        # Importar textos de fundamentos
        texto_file = os.path.join(data_dir, 'texto_fundamentos.txt')
        if os.path.exists(texto_file):
            self.stdout.write('Importando textos de fundamentos...')
            self.importar_textos(texto_file)

        # Atualizar relacionamentos pai-filho
        self.stdout.write('Atualizando relacionamentos hierárquicos...')
        self.atualizar_relacionamentos()

        total = FundamentoLegal.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Importação concluída! {total} fundamentos importados.'))

    @transaction.atomic
    def importar_csv(self, filepath, tipo_recurso):
        df = pd.read_csv(filepath, sep='#', encoding='utf-8', dtype=str)
        df = df.fillna('')
        
        registros = []
        for _, row in df.iterrows():
            try:
                seq = int(row['SEQ_FUNDAMENTO_LEGAL'])
            except (ValueError, KeyError):
                continue

            pai_seq = None
            if row.get('SEQ_FUNDAMENTO_LEGAL_PAI', '').strip():
                try:
                    pai_seq = int(row['SEQ_FUNDAMENTO_LEGAL_PAI'])
                except ValueError:
                    pai_seq = None

            descricao = row.get('DESCRICAO', '').strip()
            glossario = row.get('GLOSSARIO', '').strip() or None
            
            # Campos específicos do AFIRE
            neutro = row.get('NEUTRO', 'N') == 'S'
            informacao = row.get('INFORMACAO', 'N') == 'S'
            justificativa = row.get('JUSTIFICATIVA', 'N') == 'S'
            selecionavel = row.get('SELECIONAVEL', 'S') == 'S'

            # Determinar categoria
            categoria = Categoria.GERAL
            desc_upper = descricao.upper()
            if 'CÍVEL' in desc_upper or 'CIVEL' in desc_upper:
                categoria = Categoria.CIVEL
            elif 'CRIMINAL' in desc_upper:
                categoria = Categoria.CRIMINAL

            fundamento = FundamentoLegal(
                seq=seq,
                descricao=descricao,
                glossario=glossario,
                tipo_recurso=tipo_recurso,
                categoria=categoria,
                neutro=neutro,
                informacao=informacao,
                justificativa=justificativa,
                selecionavel=selecionavel,
            )
            registros.append((fundamento, pai_seq))

        # Primeiro, criar todos os fundamentos sem pai
        for fundamento, _ in registros:
            fundamento.save()

        # Depois, atualizar os pais
        for fundamento, pai_seq in registros:
            if pai_seq:
                try:
                    pai = FundamentoLegal.objects.get(seq=pai_seq)
                    fundamento.pai = pai
                    fundamento.save(update_fields=['pai'])
                except FundamentoLegal.DoesNotExist:
                    pass

        self.stdout.write(f'  -> {len(registros)} registros importados')

    def importar_textos(self, filepath):
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()

        # Pular cabeçalho
        for line in lines[1:]:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                try:
                    seq = int(parts[0].strip())
                    legislacao = parts[1].strip() if len(parts) > 1 else ''
                    texto_html = parts[2].strip() if len(parts) > 2 else ''
                    
                    try:
                        fundamento = FundamentoLegal.objects.get(seq=seq)
                        TextoFundamento.objects.create(
                            fundamento=fundamento,
                            legislacao=legislacao,
                            texto_html=texto_html
                        )
                    except FundamentoLegal.DoesNotExist:
                        pass
                except ValueError:
                    continue

    def atualizar_relacionamentos(self):
        """Corrige relacionamentos pai-filho após importação completa"""
        fundamentos_sem_pai = FundamentoLegal.objects.filter(
            pai__isnull=True
        ).exclude(seq__in=FundamentoLegal.objects.values_list('pai__seq', flat=True))
        
        self.stdout.write(f'  -> {fundamentos_sem_pai.count()} fundamentos raiz identificados')
