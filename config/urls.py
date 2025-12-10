from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fundamentos.urls')),
]

# Personalização do Admin
admin.site.site_header = 'STJ Fundamentos Legais'
admin.site.site_title = 'Administração'
admin.site.index_title = 'Gerenciamento de Fundamentos'
