from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.http import JsonResponse
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import FundamentoLegal, TextoFundamento, TipoRecurso, Categoria
from .serializers import (
    FundamentoLegalListSerializer,
    FundamentoLegalDetailSerializer,
    FundamentoLegalTreeSerializer,
    TextoFundamentoSerializer
)


class StandardPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


class FundamentoLegalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API para consulta de fundamentos legais do STJ.
    
    Endpoints:
    - GET /api/fundamentos/ - Lista todos os fundamentos
    - GET /api/fundamentos/{seq}/ - Detalhe de um fundamento
    - GET /api/fundamentos/arvore/ - Visualização em árvore
    - GET /api/fundamentos/busca/ - Busca textual
    - GET /api/fundamentos/estatisticas/ - Estatísticas gerais
    """
    queryset = FundamentoLegal.objects.all()
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['descricao', 'glossario']
    ordering_fields = ['seq', 'tipo_recurso', 'categoria']
    ordering = ['seq']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FundamentoLegalDetailSerializer
        return FundamentoLegalListSerializer

    def get_queryset(self):
        queryset = FundamentoLegal.objects.all()
        
        # Filtro por tipo de recurso
        tipo = self.request.query_params.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo_recurso=tipo)
        
        # Filtro por categoria
        categoria = self.request.query_params.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        
        # Filtro por selecionáveis
        selecionavel = self.request.query_params.get('selecionavel')
        if selecionavel is not None:
            queryset = queryset.filter(selecionavel=selecionavel.lower() == 'true')
        
        # Filtro apenas raízes (sem pai)
        apenas_raiz = self.request.query_params.get('raiz')
        if apenas_raiz and apenas_raiz.lower() == 'true':
            queryset = queryset.filter(pai__isnull=True)
        
        # Filtro por pai específico
        pai = self.request.query_params.get('pai')
        if pai:
            queryset = queryset.filter(pai__seq=pai)
        
        return queryset

    @action(detail=False, methods=['get'])
    def arvore(self, request):
        """Retorna fundamentos em estrutura de árvore"""
        tipo = request.query_params.get('tipo')
        
        queryset = FundamentoLegal.objects.filter(pai__isnull=True)
        if tipo:
            queryset = queryset.filter(tipo_recurso=tipo)
        
        serializer = FundamentoLegalTreeSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def busca(self, request):
        """Busca textual em descrição e glossário"""
        termo = request.query_params.get('q', '')
        if not termo or len(termo) < 2:
            return Response({'erro': 'Termo de busca deve ter pelo menos 2 caracteres'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Busca em múltiplos campos
        queryset = FundamentoLegal.objects.filter(
            Q(descricao__icontains=termo) | 
            Q(glossario__icontains=termo)
        )
        
        # Aplicar filtros adicionais
        tipo = request.query_params.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo_recurso=tipo)
        
        categoria = request.query_params.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        
        # Paginação
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FundamentoLegalListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = FundamentoLegalListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas gerais dos fundamentos"""
        stats = {
            'total': FundamentoLegal.objects.count(),
            'por_tipo': {},
            'por_categoria': {},
            'selecionaveis': FundamentoLegal.objects.filter(selecionavel=True).count(),
            'com_glossario': FundamentoLegal.objects.exclude(
                Q(glossario__isnull=True) | Q(glossario='')
            ).count(),
            'raizes': FundamentoLegal.objects.filter(pai__isnull=True).count(),
        }
        
        # Contagem por tipo de recurso
        for tipo in TipoRecurso:
            stats['por_tipo'][tipo.label] = FundamentoLegal.objects.filter(
                tipo_recurso=tipo.value
            ).count()
        
        # Contagem por categoria
        for cat in Categoria:
            stats['por_categoria'][cat.label] = FundamentoLegal.objects.filter(
                categoria=cat.value
            ).count()
        
        return Response(stats)

    @action(detail=True, methods=['get'])
    def descendentes(self, request, pk=None):
        """Retorna todos os descendentes de um fundamento"""
        fundamento = self.get_object()
        descendentes = fundamento.get_descendentes()
        serializer = FundamentoLegalListSerializer(descendentes, many=True)
        return Response(serializer.data)


# Views para interface web
def index(request):
    """Página inicial com interface de busca"""
    tipos = [{'value': t.value, 'label': t.label} for t in TipoRecurso]
    categorias = [{'value': c.value, 'label': c.label} for c in Categoria]
    
    # Estatísticas resumidas
    stats = {
        'total': FundamentoLegal.objects.count(),
        'tipos': {t.label: FundamentoLegal.objects.filter(tipo_recurso=t.value).count() 
                 for t in TipoRecurso}
    }
    
    context = {
        'tipos': tipos,
        'categorias': categorias,
        'stats': stats,
    }
    return render(request, 'fundamentos/index.html', context)


def detalhe(request, seq):
    """Página de detalhe de um fundamento"""
    fundamento = get_object_or_404(FundamentoLegal, seq=seq)
    context = {
        'fundamento': fundamento,
        'caminho': fundamento.caminho,
        'filhos': fundamento.filhos.all(),
        'textos': fundamento.textos.all(),
    }
    return render(request, 'fundamentos/detalhe.html', context)


def arvore_view(request):
    """Visualização em árvore interativa"""
    tipo = request.GET.get('tipo', TipoRecurso.AFIRE.value)
    raizes = FundamentoLegal.objects.filter(
        pai__isnull=True,
        tipo_recurso=tipo
    )
    
    tipos = [{'value': t.value, 'label': t.label} for t in TipoRecurso]
    
    context = {
        'raizes': raizes,
        'tipo_atual': tipo,
        'tipos': tipos,
    }
    return render(request, 'fundamentos/arvore.html', context)


@api_view(['GET'])
def api_filhos(request, seq):
    """API endpoint para carregar filhos de forma lazy"""
    fundamento = get_object_or_404(FundamentoLegal, seq=seq)
    filhos = fundamento.filhos.all()
    serializer = FundamentoLegalListSerializer(filhos, many=True)
    return Response(serializer.data)
