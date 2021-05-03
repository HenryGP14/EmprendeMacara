from django.urls import path

from Empresa import views

urlpatterns = [
    path('solicitar-cuenta/', views.vwTplSolicitar, name="solicitar-cuenta"),
    path('enviar-solicitud/', views.vwGrdSolicit, name="enviar-solicitud"),
]

