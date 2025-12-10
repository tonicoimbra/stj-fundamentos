from rest_framework import serializers
from .models import FundamentoLegal, TextoFundamento


class TextoFundamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextoFundamento
        fields = ['id', 'legislacao', 'texto_html']


class FundamentoLegalListSerializer(serializers.ModelSerializer):
    """Serializer compacto para listagens"""
    tem_filhos = serializers.SerializerMethodField()
    
    class Meta:
        model = FundamentoLegal
        fields = [
            'seq', 'descricao', 'tipo_recurso', 'categoria',
            'selecionavel', 'pai', 'tem_filhos'
        ]
    
    def get_tem_filhos(self, obj):
        return obj.filhos.exists()


class FundamentoLegalDetailSerializer(serializers.ModelSerializer):
    """Serializer detalhado com relacionamentos"""
    textos = TextoFundamentoSerializer(many=True, read_only=True)
    filhos = serializers.SerializerMethodField()
    caminho = serializers.SerializerMethodField()
    nivel = serializers.ReadOnlyField()
    pai_info = serializers.SerializerMethodField()
    
    class Meta:
        model = FundamentoLegal
        fields = [
            'seq', 'descricao', 'glossario', 'tipo_recurso', 'categoria',
            'neutro', 'informacao', 'justificativa', 'selecionavel',
            'pai', 'pai_info', 'filhos', 'textos', 'nivel', 'caminho',
            'criado_em', 'atualizado_em'
        ]
    
    def get_filhos(self, obj):
        return FundamentoLegalListSerializer(obj.filhos.all(), many=True).data
    
    def get_caminho(self, obj):
        return [{'seq': f.seq, 'descricao': f.descricao} for f in obj.caminho]
    
    def get_pai_info(self, obj):
        if obj.pai:
            return {'seq': obj.pai.seq, 'descricao': obj.pai.descricao}
        return None


class FundamentoLegalTreeSerializer(serializers.ModelSerializer):
    """Serializer para visualização em árvore"""
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = FundamentoLegal
        fields = ['seq', 'descricao', 'tipo_recurso', 'categoria', 'selecionavel', 'children']
    
    def get_children(self, obj):
        children = obj.filhos.all()
        return FundamentoLegalTreeSerializer(children, many=True).data
