from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.core.mail import send_mail

from Modelos.models import (
    empresas,
    activi_comerciales,
    productos,
    servicios,
    usuarios,
)
from Global.usuario import Usuario
from Cliente.carrito import Carrito

# Vista para ver el html de error, si una página no existe
def error_404_view(request, exception):
    return render(request, "error/404.html", {"error": "La página no exite"})


# Vista que retorna el html de inicio de sesión
def vwInicio(request):
    user_session = Usuario(request)
    try:
        if request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    list_categorias = activi_comerciales.objects.all()
    return render(request, "index.html", {"categorias": list_categorias})


# Vista que retorna el html de login
def vwTplLogin(request):
    user_session = Usuario(request)
    try:
        if request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    return render(request, "autenticacion/login.html")


# Vista que me permita logear, guardando los datos del cliente en una variable session
def vwLogin(request):
    user_session = Usuario(request)
    try:
        if request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    try:
        usuario = usuarios.objects.get(correo=request.POST["txtUsuario"])
        # Identifica si el usuario se encuentra habilitado, para iniciar sessión
        if not usuario.estado:
            messages.error(request, "La cuenta que estás intentando ingresar no es valida")
            return redirect("index")

        if usuario.credenciales == request.POST["txtCredenciales"]:

            # Guardar el usuario y carrito en una variable session
            user_session.add(usuario)
            cart_session = Carrito(request)
            return redirect("index")
        else:
            messages.error(request, "La contraseña es incorrecta " + usuario.nom_usuario)
        return redirect("login")
    except:
        messages.error(request, "La cuenta que estás ingresando no se encuentra registrada")
    return redirect("login")


# Vista que permite cerrar sessión, eliminando la variable session del usuario y guardando los datos del carrito en la base de datos
def vwLogout(request):
    # Cerrar sessión para cualquier usuario
    try:
        if not request.session["usuario"]:
            messages.info(request, "Debes iniciar sessión")
            return redirect("login")
    except:
        pass
    user_session = Usuario(request)
    if request.session["usuario"]["rol_id"] == 1:
        cart_session = Carrito(request)
        # Eliminar los valores de carrito y usuario session
        cart_session.clear()
    user_session.clear()
    return redirect("index")


# Vista que retorna el html para registrar un cliente
def vwTplRegistrar(request):
    user_session = Usuario(request)
    try:
        if request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    return redirect("solicitar-cuenta")


# Vista que retorna el html más la lista de empresas segun su id
def vwTplListaNegocios(request, negocio_id):
    user_session = Usuario(request)
    try:
        if request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    list_negocios = empresas.objects.filter(activi_comercial_id=negocio_id, estado="Habilitada")

    return render(request, "empresa/tplListaNegocios.html", {"empresas": list_negocios})


# Vista que carga la información del negocio según su id
def vwTplInfoNegocio(request, empresa_id):
    user_session = Usuario(request)
    try:
        if request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
    except:
        pass

    list_negocios = empresas.objects.get(pk=empresa_id, estado="Habilitada")
    return render(request, "empresa/tplInfoNegocio.html", {"empresa": list_negocios})


# Vista que carga los productos y servicos de la empresa sefún su id
def vwTplPrSrNegocio(request, empresa_id):
    user_session = Usuario(request)
    try:
        if request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass
    em_fotos_servicio = servicios.objects.filter(empresa_id=empresa_id, visible=True)

    em_fotos_producto = productos.objects.filter(empresa_id=empresa_id, visible=True)

    empresa = empresas.objects.get(pk=empresa_id, estado="Habilitada")

    return render(request, "empresa/tplPrSrNegocio.html", {"empresa": empresa, "em_fotos_servicio": em_fotos_servicio, "em_fotos_producto": em_fotos_producto})
