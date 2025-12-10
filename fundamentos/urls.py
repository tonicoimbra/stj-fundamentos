from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'fundamentos', views.FundamentoLegalViewSet, basename='fundamento')

app_name = 'fundamentos'

urlpatterns = [
    # Interface web
    path('', views.index, name='index'),
    path('detalhe/<int:seq>/', views.detalhe, name='detalhe'),
    path('arvore/', views.arvore_view, name='arvore'),
    
    # API REST
    path('api/', include(router.urls)),
    path('api/filhos/<int:seq>/', views.api_filhos, name='api_filhos'),
]
