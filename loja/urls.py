from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('produto.urls')), # vai chamar arquivo urls d pasta PRODUTO
    path('perfil/', include('perfil.urls')),  # vai chamar arquivo urls da pasta PERFIL
    path('pedido/', include('pedido.urls')),  # vai chamar arquivo urls da pasta PEDIDO
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)