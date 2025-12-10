from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import FundamentoLegal, TextoFundamento


class TextoFundamentoInline(admin.TabularInline):
    model = TextoFundamento
    extra = 0
    fields = ['legislacao', 'texto_html']


@admin.register(FundamentoLegal)
class FundamentoLegalAdmin(admin.ModelAdmin):
    list_display = [
        'seq', 'descricao_truncada', 'tipo_recurso', 'categoria', 
        'selecionavel', 'pai_link', 'num_filhos'
    ]
    list_filter = ['tipo_recurso', 'categoria', 'selecionavel', 'neutro']
    search_fields = ['seq', 'descricao', 'glossario']
    raw_id_fields = ['pai']
    readonly_fields = ['criado_em', 'atualizado_em', 'nivel_display', 'caminho_display']
    inlines = [TextoFundamentoInline]
    
    fieldsets = (
        ('Identificação', {
            'fields': ('seq', 'descricao', 'glossario')
        }),
        ('Classificação', {
            'fields': ('tipo_recurso', 'categoria', 'pai')
        }),
        ('Atributos', {
            'fields': ('selecionavel', 'neutro', 'informacao', 'justificativa')
        }),
        ('Informações', {
            'fields': ('nivel_display', 'caminho_display', 'criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _num_filhos=Count('filhos')
        )

    def descricao_truncada(self, obj):
        return obj.descricao[:80] + '...' if len(obj.descricao) > 80 else obj.descricao
    descricao_truncada.short_description = 'Descrição'

    def pai_link(self, obj):
        if obj.pai:
            return format_html(
                '<a href="/admin/fundamentos/fundamentolegal/{}/change/">[{}] {}</a>',
                obj.pai.seq, obj.pai.seq, obj.pai.descricao[:30]
            )
        return '-'
    pai_link.short_description = 'Pai'

    def num_filhos(self, obj):
        count = getattr(obj, '_num_filhos', obj.filhos.count())
        if count > 0:
            return format_html(
                '<a href="?pai__seq={}">{} filhos</a>',
                obj.seq, count
            )
        return '0'
    num_filhos.short_description = 'Filhos'
    num_filhos.admin_order_field = '_num_filhos'

    def nivel_display(self, obj):
        return obj.nivel
    nivel_display.short_description = 'Nível hierárquico'

    def caminho_display(self, obj):
        return ' → '.join([f'[{f.seq}]' for f in obj.caminho])
    caminho_display.short_description = 'Caminho'


@admin.register(TextoFundamento)
class TextoFundamentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'fundamento', 'legislacao']
    list_filter = ['fundamento__tipo_recurso']
    search_fields = ['fundamento__descricao', 'legislacao', 'texto_html']
    raw_id_fields = ['fundamento']
