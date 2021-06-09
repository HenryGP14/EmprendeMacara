from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from Global import views

urlpatterns = [
    # URL de la página de inicio de la app
    path("", views.vwInicio, name="index"),
    # URLS de de negocio
    path("negocios/<int:negocio_id>", views.vwTplListaNegocios, name="list_negocios"),
    path("negocios/fanpage/info/<int:empresa_id>", views.vwTplInfoNegocio, name="info_negocio"),
    path("negocios/fanpage/producto-servicio/<int:empresa_id>", views.vwTplPrSrNegocio, name="pr_sr_negocio"),
    # URLS de autenticación
    path("login", views.vwTplLogin, name="login"),
    path("registrar", views.vwTplRegistrar, name="registrar"),
    path("logeado", views.vwLogin, name="logear"),
    path("logout", views.vwLogout, name="logout"),
]
