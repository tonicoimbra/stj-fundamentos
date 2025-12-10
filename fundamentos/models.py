from django.db import models


class TipoRecurso(models.TextChoices):
    AFIRE = 'AFIRE', 'Fundamentos de Inadmissão REsp'
    AFIPO_RESP = 'AFIPO_RESP', 'REsp e AREsp'
    AFIPO_RMS = 'AFIPO_RMS', 'RMS - Recurso em Mandado de Segurança'
    AFIREQ = 'AFIREQ', 'Requisitos de Fundamentos'


class Categoria(models.TextChoices):
    CIVEL = 'CIVEL', 'Cível'
    CRIMINAL = 'CRIMINAL', 'Criminal'
    GERAL = 'GERAL', 'Geral'


class FundamentoLegal(models.Model):
    """
    Modelo principal para fundamentos legais do STJ.
    Estrutura hierárquica com auto-referência (pai/filhos).
    """
    seq = models.IntegerField(primary_key=True, verbose_name='Sequencial')
    pai = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='filhos',
        verbose_name='Fundamento Pai'
    )
    descricao = models.TextField(verbose_name='Descrição')
    glossario = models.TextField(blank=True, null=True, verbose_name='Glossário')
    tipo_recurso = models.CharField(
        max_length=20, 
        choices=TipoRecurso.choices,
        verbose_name='Tipo de Recurso'
    )
    categoria = models.CharField(
        max_length=20, 
        choices=Categoria.choices,
        default=Categoria.GERAL,
        verbose_name='Categoria'
    )
    
    # Campos específicos do AFIRE
    neutro = models.BooleanField(default=False, verbose_name='Neutro')
    informacao = models.BooleanField(default=False, verbose_name='Informação')
    justificativa = models.BooleanField(default=False, verbose_name='Justificativa')
    selecionavel = models.BooleanField(default=True, verbose_name='Selecionável')
    
    # Metadados
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Fundamento Legal'
        verbose_name_plural = 'Fundamentos Legais'
        ordering = ['tipo_recurso', 'seq']
        indexes = [
            models.Index(fields=['tipo_recurso']),
            models.Index(fields=['categoria']),
            models.Index(fields=['descricao']),
        ]

    def __str__(self):
        return f"[{self.seq}] {self.descricao[:80]}..."

    @property
    def nivel(self):
        """Retorna o nível hierárquico do fundamento"""
        nivel = 0
        atual = self
        while atual.pai:
            nivel += 1
            atual = atual.pai
        return nivel

    @property
    def caminho(self):
        """Retorna o caminho completo até o fundamento raiz"""
        caminho = [self]
        atual = self
        while atual.pai:
            caminho.insert(0, atual.pai)
            atual = atual.pai
        return caminho

    def get_descendentes(self):
        """Retorna todos os descendentes recursivamente"""
        descendentes = list(self.filhos.all())
        for filho in self.filhos.all():
            descendentes.extend(filho.get_descendentes())
        return descendentes


class TextoFundamento(models.Model):
    """
    Textos em HTML associados aos fundamentos legais.
    """
    fundamento = models.ForeignKey(
        FundamentoLegal,
        on_delete=models.CASCADE,
        related_name='textos',
        verbose_name='Fundamento'
    )
    legislacao = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name='Legislação'
    )
    texto_html = models.TextField(verbose_name='Texto em HTML')
    
    class Meta:
        verbose_name = 'Texto de Fundamento'
        verbose_name_plural = 'Textos de Fundamentos'

    def __str__(self):
        return f"Texto para fundamento {self.fundamento.seq}"
