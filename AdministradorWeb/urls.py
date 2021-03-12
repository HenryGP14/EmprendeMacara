from django.urls import path

from AdministradorWeb import views

urlpatterns = [
    # URL PARA MOSTRAR PLANTILLAS
    path('admin-web/', views.vwTplMenuAdmin, name="admin-web"),
    path('empresas/', views.vwTplEmpresas, name="empresas"),
    path('solicitudes/', views.vwTplSolicitudes, name="solicitudes"),
    path('perfil-admin/', views.vwTplPerfil, name="perfil-admin"),
    # URL DE ACCIONES
    path('save-perfil/', views.vwGrdPerfil, name="save-perfil"),
    path('get-empresas/', views.vwgetEmpresas, name="get-empresas"),
    path('get-solicitudes/', views.vwgetSolicitudes, name="get-solicitudes"),
    path('cambiar-estado/', views.vwCambiarEstado, name="cambiar-estado"),
    path('aceptar-solicitud/', views.vwAceptarSolici, name="aceptar-solicitud"),
    path('rechazar-solicitud/', views.vwRechazarSolici, name="rechazar-solicitud"),
    path('buscar-solicitud/', views.vwBusSolicitud, name="buscar-solicitud"),
    path('buscar-empresa/', views.vwBusEmpresa, name="buscar-empresa"),
]
