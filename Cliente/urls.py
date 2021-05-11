from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from Cliente import views

urlpatterns = [
    # URLS carrito
    path('carrito', views.vwTplCarrito, name="carrito"),
    path('add-producto/<int:producto_id>',
         views.vwAggPrCart, name="add-producto"),
    path('clear-carrito', views.vwClsCarrito, name="clear-carrito"),
    path('incrementar-producto', views.vwIncrementarPrCart, name="incrementar-pr"),
    path('decrementar-producto', views.vwDecrementarPrCart, name="decrementar-pr"),
    path('remove-producto/<int:producto_id>',
         views.vwElmProductoCart, name="remove-producto"),
    # URLS compra
    path('detalles-de-facturacion/<int:producto_id>',
         views.vwTplDtFactura, name="factura"),
    path('registrar-pedido', views.vwRegPedido, name="registrar_pedido")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
