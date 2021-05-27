from django.urls import path

from AdministradorWeb import views

urlpatterns = [
    # URL PARA MOSTRAR PLANTILLAS
    path('admin-web/', views.vwTplMenuAdmin, name="admin-web"),
    path('empresas/', views.vwTplEmpresas, name="empresas"),
    path('solicitudes/', views.vwTplSolicitudes, name="solicitudes"),
    path('perfil-admin/', views.vwTplPerfil, name="perfil-admin"),
    path('act-comerciales', views.vwTplActComercial, name="act-comerciales"),
    # URL DE ACCIONES
    path('save-perfil/', views.vwGrdPerfil, name="save-perfil"),
    path('registrar-actividad-comercial/', views.vwGrdActComercial, name="registrar-actividad-comercial"),
    path('modificar-actividad-comercial/', views.vwEdiActComercial, name="modificar-actividad-comercial"),
    path('eliminar-actividad-comercial/', views.vwEliActComercial, name="eliminar-actividad-comercial"),
    path('habilitar-actividad-comercial/', views.vwHabiliActivi, name="habilitar-actividad-comercial"),
    path('deshabilitar-actividad-comercial/', views.vwDeshabiliActi, name="deshabilitar-actividad-comercial"),
    path('get-empresas/', views.vwgetEmpresas, name="get-empresas"),
    path('get-solicitudes/', views.vwgetSolicitudes, name="get-solicitudes"),
    path('cambiar-estado/', views.vwCambiarEstado, name="cambiar-estado"),
    path('aceptar-solicitud/', views.vwAceptarSolici, name="aceptar-solicitud"),
    path('rechazar-solicitud/', views.vwRechazarSolici, name="rechazar-solicitud"),
    path('buscar-solicitud/', views.vwBusSolicitud, name="buscar-solicitud"),
    path('buscar-empresa/', views.vwBusEmpresa, name="buscar-empresa"),
]
