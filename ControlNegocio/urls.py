from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from ControlNegocio import views

urlpatterns = [ 
    # URL PARA MOSTRAR PLANTILLAS
    path('controlNegocio', views.vwOpcPedidosPendientes, name="controlNegocio"),
    path('PedidosEntregados', views.vwOpcPedidosEntregados, name="PedidosEntregados"),
    path('PedidosPendientes', views.vwOpcPedidosPendientes, name="PedidosPendientes"),
    path('ProductosServicios/', views.vwOpcProductosServicios, name="ProductosServicios"),
    path('perfil', views.vwTplPerfil, name="perfil"),
    path('ConfiguracionEmpresa', views.vwConfiguracionEmpresa, name="ConfiguracionEmpresa"),
    #==============URL  ELIMINAR==============
    path('eliminarProducto/', views.vwEliminarProducto, name="eliminarProducto"),
    path('eliminarServicio/', views.vwEliminarServicio, name="eliminarServicio"),
    #==============URL HABILITAR==============
    path('habilitarProducto/', views.vwHabilitarProducto, name="habilitarProducto"),
    path('habilitarServicio/', views.vwHabilitarServicio, name="habilitarServicio"),
    #==============URL DESHABILITAR================
    path('deshabilitarProducto/', views.vwDeshabilitarProducto, name="deshabilitarProducto"),
    path('deshabilitarServicio/', views.vwDeshabilitarServicio, name="deshabilitarServicio"),
    #==============URL GUARDAR==================
    path('anadirProducto', views.vwAnadirProducto, name="anadirProducto"),
    path('anadirServicio', views.vwAnadirServicio, name="anadirServicio"),
    #==============URL EDITAR==================
    path('editarProducto', views.vwEditarProducto, name="editarProducto"),
    path('editarServicio', views.vwEditarServicio, name="editarServicio"),
    path('guardar-perfil-empresa', views.vwSaveFotoEmpresa, name="guardar-perfil-empresa"),
    path('savename', views.vwsaveName, name="savename"),
    path('savepass', views.vwsavepass, name="savepass"),
    #============URL OBTENER OBJETO=============
    path('obtenerServicio', views.vwObtenerServicio,name="obtenerServicio"),
    path('obtenerProducto', views.vwObtenerProducto,name="obtenerProducto"),
    path('obtenerDetalleVenta', views.vwObtenerDetalleVenta,name="obtenerDetalleVenta"),
    path('obtenerPago', views.vwObtenerPago,name="obtenerPago"),
    #===========URL PEDIDOS ESTADOS========
    path('entregarPedido', views.vwEntregarPedido,name="entregarPedido"),
    path('anularPedido', views.vwAnularPedido,name="anularPedido"),
    path('EnviarPedido', views.vwEnviarPedido,name="EnviarPedido"),
    
    # OPCIÓN DE MODIFICAR PERFIL DE LA EMPRESA
    path('delete-foto', views.vwElmFoto,name="delete-foto"),
    path('save-foto-carousel', views.vwGrdFoto,name="save-foto-carousel"),
    path('editar-perfil', views.vwEdtPerfil, name="editar-perfil"),
    path('editar-foto-perfil', views.vwGuardarFoto, name="editar-foto-perfil"),
    path('editar-foto-portada', views.vwGuardarPortada, name="editar-foto-portada"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)