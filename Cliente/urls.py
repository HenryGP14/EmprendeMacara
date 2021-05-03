from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from Cliente import views

urlpatterns = [
    # URLS clientes
    path('configuraciones', views.vwTplConfiguracion, name="configuraciones"),
    path('guardar-credenciales', views.vwGrdCredenciales, name="guardar-pass"),
    path('guardar-perfil', views.vwGrdPerfil, name="guardar-perfil"),
    path('guardar-nombre', views.vwGrdNombre, name="guardar-nombre"),
    path('registrando-cliente', views.vwRegCliente, name="registrando-cliente"),
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
    path('registrar-pedido', views.vwRegPedido, name="registrar_pedido"),
    # URLS pedidos
    path('pedidos', views.vwTplPedidos, name="pedidos"),
    path('pedidos-detalles', views.vwObtenerDtPed, name="detalles_pedidos")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
