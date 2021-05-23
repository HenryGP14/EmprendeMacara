from django.shortcuts import render, redirect
from django.http import JsonResponse
from Modelos.models import empresas, telefo_empresas, usuarios
from django.db import transaction
from django.contrib import messages
from Global.usuario import Usuario
from Global.correo import Correo
import os

# Vista que redirecciona a la plantilla de empresas
def vwTplMenuAdmin(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"]:
            messages.info(request, "Debes iniciar sessión para administrar la página")
            return redirect("login")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
    except:
        pass
    return redirect("empresas")


# Vista que renderiza la plantilla de lista de empresas
def vwTplEmpresas(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
    except:
        pass
    # Se envía la clase css activado para que en el menú quede seleccionada la opción
    datos = {"lista_active": "activado"}
    return render(request, "tplListaEmpresas.html", context={"datos": datos})


# Vista que renderiza la plantilla que muestra la solicitudes que empresas que desean ser parte de Emprendimientos Macará
def vwTplSolicitudes(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
    except:
        pass
    # Se envía la clase css activado para que en el menú quede seleccionada la opción
    datos = {"solicitud_active": "activado"}
    return render(request, "tplSolicitudes.html", context={"datos": datos})


# Vista que renderiza la plantilla que muestra los datos del perfil del administrador
def vwTplPerfil(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
    except:
        pass
    usuario_id = int(request.session["usuario"]["id"])
    unUsuario = usuarios.objects.get(id=usuario_id)
    # Se envía la clase css activado para que en el menú quede seleccionada la opción y se envían los datos del usuario administrador
    datos = {"perfil_active": "activado", "unUsuario": unUsuario}
    return render(request, "tplPerfilAdmin.html", context={"datos": datos})


# Vista que guarda los cambios en los datos del administrador
def vwGrdPerfil(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
    except:
        pass
    if request.method == "POST":
        try:
            with transaction.atomic():
                usuario_id = int(request.session["usuario"]["id"])
                unUsuario = usuarios.objects.get(id=usuario_id)
                # Ingresa si se cambió la contraseña
                if request.POST["txtContraActul"] != "" or request.POST["txtNewContra"] != "" or request.POST["txtConfirContra"] != "":
                    if request.POST["txtContraActul"] == unUsuario.credenciales:
                        if request.POST["txtContraActul"] != request.POST["txtNewContra"]:
                            unUsuario.credenciales = request.POST["txtNewContra"]
                            unUsuario.correo = request.POST["txtUsuario"]
                            unUsuario.nom_usuario = request.POST["txtAdministrador"]
                            try:
                                imgBorrar = "media\\" + unUsuario.ruta_foto.name
                                unUsuario.ruta_foto = request.FILES["imgFoto"]
                                a, b = os.path.splitext(unUsuario.ruta_foto.name)
                                unUsuario.ruta_foto.name = "PerfilAdministrador" + str(unUsuario.id) + b
                                os.remove(imgBorrar)
                            except Exception as e:
                                pass

                            unUsuario.save()
                            user_session.edit_nombre(unUsuario.nom_usuario)
                            try:
                                user_session.edit_perfil(unUsuario.ruta_foto)
                            except Exception as e:
                                pass
                            # Se envia cambioUserContra = si, para mostrar un mensaje que se cerrará la sesión y al aceptar se cierra la sesión
                            return JsonResponse({"result": "1", "cambioUserContra": "si"})
                        else:
                            return JsonResponse({"result": "La nueva contraseña debe ser diferente a la actual"})
                    else:
                        return JsonResponse({"result": "La contraseña actual no es la correcta"})
                # Ingresa si se cambió el usuario
                elif request.POST["txtUsuario"] != unUsuario.correo:
                    unUsuario.correo = request.POST["txtUsuario"]
                    unUsuario.nom_usuario = request.POST["txtAdministrador"]
                    try:
                        imgBorrar = "media\\" + unUsuario.ruta_foto.name
                        unUsuario.ruta_foto = request.FILES["imgFoto"]
                        a, b = os.path.splitext(unUsuario.ruta_foto.name)
                        unUsuario.ruta_foto.name = "PerfilAdministrador" + str(unUsuario.id) + b
                        os.remove(imgBorrar)
                    except Exception as e:
                        pass
                    unUsuario.save()
                    user_session.edit_nombre(unUsuario.nom_usuario)
                    try:
                        user_session.edit_perfil(unUsuario.ruta_foto)
                    except Exception as e:
                        pass
                    # Se envia cambioUserContra = si, para mostrar un mensaje que se cerrará la sesión y al aceptar se cierra la sesión
                    return JsonResponse({"result": "1", "cambioUserContra": "si"})
                # Ingresa si se cambio el nombre de usuario o foto de perfil
                else:
                    unUsuario.nom_usuario = request.POST["txtAdministrador"]
                    try:
                        imgBorrar = "media\\" + unUsuario.ruta_foto.name
                        unUsuario.ruta_foto = request.FILES["imgFoto"]
                        a, b = os.path.splitext(unUsuario.ruta_foto.name)
                        unUsuario.ruta_foto.name = "PerfilAdministrador" + str(unUsuario.id) + b
                        os.remove(imgBorrar)
                    except Exception as e:
                        pass
                    unUsuario.save()
                    user_session.edit_nombre(unUsuario.nom_usuario)
                    try:
                        user_session.edit_perfil(unUsuario.ruta_foto)
                    except Exception as e:
                        pass
                    return JsonResponse({"result": "1", "cambioUserContra": "no"})

        except Exception as e:
            return JsonResponse({"result": "0"})


# Vista que retorna las empresas de acuerdo a un estado seleccionado
def vwgetEmpresas(request):
    try:
        user_session = Usuario(request)
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
    except:
        pass
    if request.method == "POST":
        try:
            lsEmpresas = None
            jsonEmpresas = {}
            jsonEmpresas["empresa"] = []
            lsEmpresas = empresas.objects.filter(estado=request.POST["estado"])
            for e in lsEmpresas:
                telefonos = telefo_empresas.objects.filter(empresa=e)
                crearJson(request, jsonEmpresas, e, telefonos)
            return JsonResponse({"jsonEmpresas": jsonEmpresas})
        except Exception as e:
            return JsonResponse({"jsonEmpresas": "0"})


# Vista que busca empresas por nombre del gerente o nombre de la empresas en función de un estado
def vwBusEmpresa(request):
    try:
        user_session = Usuario(request)
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
    except:
        pass
    if request.method == "POST":
        try:
            lsEmpresas = None
            jsonEmpresas = {}
            jsonEmpresas["empresa"] = []
            txtBusc = request.POST["txtBuscador"]
            lsEmpresas = empresas.objects.filter(estado=request.POST["cmbEstados"])
            for e in lsEmpresas:
                if (((e.nom_empresa.lower()).find(txtBusc.lower())) != -1) or (((e.gerente.lower()).find(txtBusc.lower())) != -1):
                    telefonos = telefo_empresas.objects.filter(empresa=e)
                    crearJson(request, jsonEmpresas, e, telefonos)
            return JsonResponse({"jsonEmpresas": jsonEmpresas})
        except Exception as e:
            return JsonResponse({"jsonEmpresas": "0"})


# Vista que retorna las solicitudes de las empresas
def vwgetSolicitudes(request):
    try:
        user_session = Usuario(request)
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
    except:
        pass
    if request.method == "POST":
        try:
            lsEmpresas = None
            jsonEmpresas = {}
            jsonEmpresas["empresa"] = []
            lsEmpresas = empresas.objects.filter(estado="Solicitante")
            for e in lsEmpresas:
                telefonos = telefo_empresas.objects.filter(empresa=e)
                crearJson(request, jsonEmpresas, e, telefonos)
            return JsonResponse({"jsonEmpresas": jsonEmpresas})
        except Exception as e:
            return JsonResponse({"jsonEmpresas": "0"})


# Vista que busca solicitudes de empresas
def vwBusSolicitud(request):
    try:
        user_session = Usuario(request)
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
    except:
        pass
    if request.method == "POST":
        try:
            lsEmpresas = None
            jsonEmpresas = {}
            jsonEmpresas["empresa"] = []
            txtBusc = request.POST["txtBuscador"]
            lsEmpresas = empresas.objects.filter(estado="Solicitante")
            for e in lsEmpresas:
                if (((e.nom_empresa.lower()).find(txtBusc.lower())) != -1) or (((e.gerente.lower()).find(txtBusc.lower())) != -1):
                    telefonos = telefo_empresas.objects.filter(empresa=e)
                    crearJson(request, jsonEmpresas, e, telefonos)
            return JsonResponse({"jsonEmpresas": jsonEmpresas})
        except Exception as e:
            return JsonResponse({"jsonEmpresas": "0"})


def crearJson(request, jsonEmpresas, e, telefonos):
    txtTelefonos = ""
    for t in telefonos:
        txtTelefonos = txtTelefonos + str(t.telefono) + "  "
    jsonEmpresas["empresa"].append(
        {
            "id_empresa": e.id,
            "empresa": e.nom_empresa,
            "gerente": e.gerente,
            "ruc": e.ruc,
            "activ_comercial": e.activi_comercial.nombre,
            "direccion": e.direccion,
            "atencion": "De " + str(e.inicio_atencion) + " a " + str(e.fin_atencion),
            "slogan": e.slogan,
            "politicas": e.politicas,
            "telefonos": txtTelefonos,
            "correo": e.correo,
            "estado": e.estado.strip(),
        }
    )


# Vista que cambia el estado de una empresa: Habilitada o Deshabilitada
def vwCambiarEstado(request):
    try:
        user_session = Usuario(request)
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
    except:
        pass
    if request.method == "POST":
        try:
            with transaction.atomic():
                unaEmpresa = empresas.objects.get(id=request.POST["id_empresa"])
                unaEmpresa.estado = request.POST["estado_empresa"]
                unaEmpresa.save()
                return JsonResponse({"result": "1"})
        except Exception as e:
            return JsonResponse({"result": "0"})


# Vista acepta la solicitud de una empresa
def vwAceptarSolici(request):
    try:
        user_session = Usuario(request)
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
    except:
        pass
    if request.method == "POST":
        try:
            with transaction.atomic():
                unaEmpresa = empresas.objects.get(id=request.POST["id_empresa"])
                unaEmpresa.estado = "Habilitada"
                unUsuario = usuarios.objects.get(id=(unaEmpresa.usuario.id))
                unUsuario.estado = True
                asunto = "Solicitud de cuenta en Emprendimientos Macará"
                mensaje = (
                    "Estimado(a) "
                    + unaEmpresa.gerente.upper()
                    + " gracias por elegirnos, su solicitud fue aceptada y ahora su empresa "
                    + unaEmpresa.nom_empresa.upper()
                    + " es parte de Emprendimientos Macará , a continuación le recordamos su usuario y contraseña:"
                )
                unCorreo = Correo(request)
                context = {"mensaje": mensaje, "linea2": "Usuario: " + unaEmpresa.usuario.correo, "linea3": "Contrseña: " + unaEmpresa.usuario.credenciales}
                # La empresa y el usuario se habilita si el correo se envía correctamente
                if unCorreo.send(unaEmpresa.correo, asunto, "components/correo.html", context):
                    unaEmpresa.save()
                    unUsuario.save()
                    return JsonResponse({"result": "1"})
                else:
                    return JsonResponse({"result": "0"})
        except Exception as e:
            return JsonResponse({"result": "0"})


# Vista que rechaza la solicitud de una empresa
def vwRechazarSolici(request):
    try:
        user_session = Usuario(request)
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
    except:
        pass
    if request.method == "POST":
        try:
            with transaction.atomic():
                unaEmpresa = empresas.objects.get(id=request.POST["id_empresa"])
                asunto = "Solicitud de cuenta en Emprendimientos Macará"
                mensaje = (
                    "Estimado(a) " + unaEmpresa.gerente.upper() + " su solicitud para que su empresa " + unaEmpresa.nom_empresa.upper() + " pueda ser parte de Emprendimientos Macará fue rechazada."
                )
                unUsuario = usuarios.objects.get(id=(unaEmpresa.usuario.id))
                unCorreo = Correo(request)
                context = {"mensaje": mensaje, "linea2": "Motivo", "linea3": request.POST["motivo"]}
                # La empresa y el usuario se eliminan si el correo se envía correctamente
                if unCorreo.send(unaEmpresa.correo, asunto, "components/correo.html", context):
                    lsTelefonos = telefo_empresas.objects.filter(empresa=unaEmpresa)
                    for t in lsTelefonos:
                        t.delete()
                    unaEmpresa.delete()
                    unUsuario.delete()
                    return JsonResponse({"result": "1"})
                else:
                    return JsonResponse({"result": "0"})
        except Exception as e:
            return JsonResponse({"result": "0"})

