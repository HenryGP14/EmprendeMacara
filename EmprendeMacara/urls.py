from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('Global.urls')),
    path('admin/', admin.site.urls),
    path('empresa/', include('Empresa.urls')),
    path('administradorWeb/', include('AdministradorWeb.urls')),
    path('cliente/', include('Cliente.urls')),
    path('negocio/', include('ControlNegocio.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'Global.views.error_404_view'
