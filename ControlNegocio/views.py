from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import transaction
from Modelos.models import (
    productos,
    empresas,
    servicios,
    ventas,
    detalles_venta,
    activi_comerciales,
    telefo_empresas,
    cuentas_bancarias,
    usuarios,
    fotos_empresas,
)
from django.db.models import Sum
import os
from django.core.serializers import serialize
from django.contrib import messages
from Global.usuario import Usuario
from django.db.models import Q

# =========VISTAS MOSTRAR PLANILLA============


def vwOpcPedidosPendientes(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"]:
            messages.info(
                request, "Debes iniciar sessión para ingresar a la página")
            return redirect("login")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
        elif request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
    except:
        pass

    unEmpresa = empresas.objects.get(
        usuario_id=request.session["usuario"]["id"])
    ltVentas = []
    for unVenta in ventas.objects.filter((Q(estado="Pendiente") | Q(estado="Enviado")) & Q(empresa_id=unEmpresa.id)):
        ltVentas.append(
            {
                "idVenta": unVenta.id,
                "nombre": unVenta.cliente,
                "direccion_entrega": unVenta.direccion_entrega,
                "telefono": unVenta.celular,
                "tipoPago": unVenta.tipo_de_pago,
                "estado": unVenta.estado,
                "numproductos": detalles_venta.objects.filter(venta_id=unVenta.id).aggregate(Sum("cantidad"))["cantidad_sum"],
                "Montototal": detalles_venta.objects.filter(venta_id=unVenta.id).aggregate(Sum("precio_unitario"))["precio_unitario_sum"],
            }
        )
    return render(
        request,
        "OpcControlNegocio/pedidosPendientes.html",
        {
            "ltVentas": ltVentas,
            "numPedidos": len(ltVentas),
            "numProductosTotales": sum(item["numproductos"] for item in ltVentas),
            "SumaMontoTotales": sum(item["Montototal"] for item in ltVentas),
            "unEmpresa": unEmpresa,
            "pendientes": "activado",
        },
    )


def vwOpcPedidosEntregados(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    unEmpresa = empresas.objects.get(
        usuario_id=request.session["usuario"]["id"])
    ltVentas = []
    for unVenta in ventas.objects.filter(empresa_id=unEmpresa.id, estado="Entregado"):
        detalle = detalles_venta.objects.filter(venta_id=unVenta.id).first()
        ltVentas.append(
            {
                "nombre": unVenta.cliente,
                "direccion_entrega": unVenta.direccion_entrega,
                "telefono": unVenta.celular,
                "tipoPago": unVenta.tipo_de_pago,
                "producto": productos.objects.get(id=detalle.producto.id).nombre,
                "cantidad": detalle.cantidad,
                "precioU": detalle.precio_unitario,
                "precioSub": detalle.cantidad * detalle.precio_unitario,
                "precioE": detalle.precio_envio,
                "Montototal": (detalle.cantidad * detalle.precio_unitario) + detalle.precio_envio,
            }
        )
    return render(
        request,
        "OpcControlNegocio/pedidosEntregados.html",
        {
            "ltVentas": ltVentas,
            "Monto": sum(item["Montototal"] for item in ltVentas),
            "cantidadTotal": sum(item["cantidad"] for item in ltVentas),
            "unEmpresa": unEmpresa,
            "entregados": "activado",
        },
    )


def vwOpcProductosServicios(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    unEmpresa = empresas.objects.get(
        usuario_id=request.session["usuario"]["id"])
    ltProductos = productos.objects.filter(empresa_id=unEmpresa.id)
    ltServicios = servicios.objects.filter(empresa_id=unEmpresa.id)
    return render(
        request,
        "OpcControlNegocio/productosServicios.html",
        {"ltProductos": ltProductos, "ltServicios": ltServicios,
            "unEmpresa": unEmpresa, "productos": "activado", "empresa_id": unEmpresa.id},
    )

# ========VISTA ELIMINAR=======


def vwEliminarProducto(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass
    try:
        unProducto = productos()
        unProducto = productos.objects.get(id=request.POST['producto_id'])
        unProducto.eliminado = True
        unProducto.save()
        return JsonResponse({"result": "1"})
    except:
        return JsonResponse({"result": "0"})


def vwEliminarServicio(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass
    try:
        unServicio = servicios()
        unServicio = servicios.objects.get(id=request.POST['servicio_id'])
        unServicio.eliminado = True
        unServicio.save()
        return JsonResponse({"result": "1"})
    except:
        return JsonResponse({"result": "0"})

# ========VISTA HABILITAR=======


def vwHabilitarServicio(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass
    try:
        unServicio = servicios()
        unServicio = servicios.objects.get(id=request.POST['servicio_id'])
        unServicio.visible = True
        unServicio.save()
        return JsonResponse({"result": "1"})
    except:
        return JsonResponse({"result": "0"})



def vwHabilitarProducto(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass
    try:
        unProducto = productos()
        unProducto = productos.objects.get(id=request.POST['producto_id'])
        unProducto.visible = True
        unProducto.save()
        return JsonResponse({"result": "1"})
    except:
        return JsonResponse({"result": "0"})

# ========VISTAS DESHABILITAR=======


def vwDeshabilitarProducto(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass
    try:
        unProducto = productos()
        unProducto = productos.objects.get(id=request.POST['producto_id'])
        unProducto.visible = False
        unProducto.save()
        return JsonResponse({"result": "1"})
    except:
        return JsonResponse({"result": "0"})


def vwDeshabilitarServicio(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    try:
        unServicio = servicios()
        unServicio = servicios.objects.get(id=request.POST['servicio_id'])
        unServicio.visible = False
        unServicio.save()
        return JsonResponse({"result": "1"})
    except:
        return JsonResponse({"result": "0"})

# =========VISTAS GUARDAR============


def vwAnadirProducto(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    if request.method == "POST":
        unEmpresa = empresas.objects.get(
            usuario_id=request.session["usuario"]["id"])

        unProducto = productos()
        unProducto.empresa = unEmpresa
        unProducto.nombre = request.POST["txtNombre"]
        unProducto.descripcion = request.POST["txtDescripcion"]
        unProducto.cantidad = int(request.POST["txtCantidad"])
        unProducto.precio_unitario = float(request.POST["txtPrecUnit"])
        unProducto.ruta_foto = request.FILES["imgFoto"]
        unProducto.visible = True
        a, b = os.path.splitext(unProducto.ruta_foto.name)
        unProducto.ruta_foto.name = "Pro_E" + str(unProducto.empresa.id) + b
        unProducto.save()
        return JsonResponse({"result": "1"})
    return JsonResponse({"result": "0"})


def vwAnadirServicio(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    if request.method == "POST":
        unEmpresa = empresas.objects.get(
            usuario_id=request.session["usuario"]["id"])

        unServicio = servicios()
        unServicio.empresa = unEmpresa
        unServicio.nombre = request.POST["txtNombre"]
        unServicio.descripcion = request.POST["txtDescripcion"]
        unServicio.ruta_foto = request.FILES["imgFotoServicio"]
        unServicio.visible = True
        a, b = os.path.splitext(unServicio.ruta_foto.name)
        unServicio.ruta_foto.name = "Serv_E" + str(unServicio.empresa.id) + b
        unServicio.save()
        return JsonResponse({"result": "1"})
    return JsonResponse({"result": "0"})


# =========VISTA OBTENER OBJECTO=======


def vwObtenerDetalleVenta(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    ltDetalleVenta = []
    for item in detalles_venta.objects.filter(venta_id=request.POST["idVenta"]).select_related("producto"):
        ltDetalleVenta.append(
            {
                "producto": item.producto.nombre,
                "descripcion": item.producto.descripcion,
                "cantidad": item.cantidad,
                "precioUni": item.precio_unitario,
                "precioSubT": item.precio_sub_total,
                "precioEnvio": item.precio_envio,
                "precioPagar": item.precio_sub_total + item.precio_envio,
                "deposito_ban": "Transferencia bancaria" if item.ruta_foto else "Pago en efectivo",
            }
        )
    return JsonResponse({"ltDetalleVenta": ltDetalleVenta})


def vwObtenerServicio(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    unServicio = servicios()
    unServicio = servicios.objects.get(id=request.POST["idServicio"])

    return JsonResponse(
        {
        "empresa": unServicio.empresa.id, 
        "nombre": unServicio.nombre, 
        "descripcion": unServicio.descripcion,
        "ruta_foto": "/media/" + unServicio.ruta_foto.name, 
        "visible": unServicio.visible,
        "servicio_id": unServicio.id,
        }
    )


def vwObtenerProducto(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    unProducto = productos.objects.get(id=request.POST["idProducto"])
    return JsonResponse(
        {
            "empresa": unProducto.empresa.id,
            "nombre": unProducto.nombre,
            "descripcion": unProducto.descripcion,
            "cantidad": unProducto.cantidad,
            "precio_unitario": unProducto.precio_unitario,
            "ruta_foto": "/media/" + unProducto.ruta_foto.name,
            "visible": unProducto.visible,
            "producto_id": unProducto.id,
        }
    )


def vwObtenerPago(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    idventa = request.POST["idventa"]
    pago = detalles_venta()
    pago = detalles_venta.objects.filter(venta_id=idventa).first()
    return JsonResponse(
        {
            "precioPagar": pago.precio_sub_total + pago.precio_envio,
            "metodoPago": "Transferencia bancaria en el " + pago.entidad_bancaria,
            "num_documento": pago.num_documento,
            "foto": pago.ruta_foto.url,
        }
    )


# =========VISTA EDITAR OBJECTO=======


def vwEditarProducto(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    unProducto = productos.objects.get(id=request.POST['producto_id'])

    unEmpresa = empresas.objects.get(
        usuario_id=request.session["usuario"]["id"])

    unProducto.empresa = unEmpresa
    unProducto.nombre = request.POST["EditNombreProducto"]
    unProducto.descripcion = request.POST["EditDescripcionProducto"]
    unProducto.cantidad = int(request.POST["EditCantidadProducto"])
    unProducto.precio_unitario = float(request.POST["EditPrecUnitProducto"])

    ruta = unProducto.ruta_foto.name
    try:
        unProducto.ruta_foto = request.FILES["inputeditproducto"]
        a, b = os.path.splitext(unProducto.ruta_foto.name)
        unProducto.ruta_foto.name = "Pro_E" + str(unEmpresa.id) + b
        os.remove('media/'+ruta)
    except:
        pass
    unProducto.visible = True
    unProducto.save()
    return JsonResponse({"result": "1"})


def vwEditarServicio(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    unServicio = servicios.objects.get(id=request.POST['id_servicio'])

    unEmpresa = empresas.objects.get(
        usuario_id=request.session["usuario"]["id"])

    unServicio.empresa = unEmpresa
    unServicio.nombre = request.POST["EditNombreServicio"]
    unServicio.descripcion = request.POST["EditDescripcionServicio"]

    ruta = unServicio.ruta_foto.name
    try:
        unServicio.ruta_foto = request.FILES["inputeditservicio"]
        a, b = os.path.splitext(unServicio.ruta_foto.name)
        unServicio.ruta_foto.name = "Serv_E" + str(unEmpresa.id) + b
        os.remove('media/'+ruta)
    except:
        print("no existe foto")
    unServicio.visible = True
    unServicio.save()
    return JsonResponse({"result": "1"})


def vwEnviarPedido(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    idventa = request.POST["idventa"]
    venta = ventas.objects.get(id=idventa)
    venta.estado = "Enviado"
    venta.save()
    return JsonResponse({"result": 1})


def vwEntregarPedido(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    idventa = request.POST["idventa"]
    venta = ventas.objects.get(id=idventa)
    venta.estado = "Entregado"
    venta.save()
    return JsonResponse({"result": 1})


def vwAnularPedido(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    idventa = request.POST["idventa"]
    venta = ventas.objects.get(id=idventa)
    venta.estado = "Anulado"
    venta.save()
    return JsonResponse({"result": 1})


def vwConfiguracionEmpresa(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    unEmpresa = empresas.objects.get(
        usuario_id=request.session["usuario"]["id"])
    return render(request, "OpcControlNegocio/ConfiguracionEmpresa.html", {"unEmpresa": unEmpresa})


def vwsaveName(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    idus = empresas.objects.get(id=request.session["usuario"]["id"])
    usuario = usuarios()
    usuario = usuarios.objects.get(pk=idus.usuario.id)
    usuario.nom_usuario = request.POST["user_nombre"]
    usuario.save()
    user_session.edit_nombre(usuario.nom_usuario)
    return JsonResponse({"redirect": ""})


def vwsavepass(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    try:
        usuario = usuarios.objects.get(pk=request.session["usuario"]["id"])
        if usuario.credenciales == request.POST["txtCredenciales"]:
            usuario.credenciales = request.POST["txtCredenciales_new"]
            usuario.save()
        else:
            messages.error(
                request, "!Ups¡ La contraseña antigua que ingresaste no es la correcta")
            return JsonResponse({"redirect": "ConfiguracionEmpresa"})
    except:
        messages.error(
            request, "!Ups¡ Tuvimos problemas al cambiar la contraseña")
        return JsonResponse({"redirect": "ConfiguracionEmpresa"})
    messages.success(
        request, "Felicitaciones. Tu contraseña se cambio correctamente, inicia sessión para confirmar")
    return JsonResponse({"redirect": "\logout"})


def vwSaveFotoEmpresa(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    idus = empresas.objects.get(id=request.session["usuario"]["id"])

    usuario = usuarios()
    usuario = usuarios.objects.get(pk=idus.usuario.id)

    usuario.ruta_foto = request.FILES.get("image")
    nom_foto, tipo_foto = os.path.splitext(usuario.ruta_foto.name)
    usuario.ruta_foto.name = "empre_perfil_" + \
        str(request.session["usuario"]["id"]) + tipo_foto
    usuario.save()
    try:
        if request.session["usuario"]["perfil"]:
            os.remove(request.session["usuario"]["perfil"][1:])
    except:
        pass
    user_session.edit_perfil(usuario.ruta_foto)
    return JsonResponse({"redirect": ""})


# Vistas de la opción de modificar los datos del perfil de la empresa

# Vista que renderiza la plantilla del perfil de la empresa
def vwTplPerfil(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    unEmpresa = empresas.objects.get(
        usuario_id=request.session["usuario"]["id"])
    fotos = fotos_empresas.objects.filter(empresa=unEmpresa)
    actividadesCom = activi_comerciales.objects.all()
    unEmpresa.costo_envio = str(unEmpresa.costo_envio).replace(",", ".")
    return render(request, "OpcControlNegocio/tplPerfil.html", {"unEmpresa": unEmpresa, "actividadesCom": actividadesCom, "perfil": "activado", "fotos": fotos})


# Vista que edita los datos del perfil de la empresa
def vwEdtPerfil(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    try:
        with transaction.atomic():
            correoEmpresa = empresas.objects.filter(
                correo=request.POST["txtCorreo"])
            if len(correoEmpresa) > 1:
                return JsonResponse({"result": "El correo de la empresa ya encuentra registrado, por favor ingrese otro usuario"})
            else:
                # Se obtienen los datos de la empresa logeada
                unaEmpresa = empresas.objects.get(
                    usuario_id=request.session["usuario"]["id"])
                # Se modifican los datos de la empresa
                unaEmpresa.ruc = request.POST["txtRuc_ci"]
                unaEmpresa.nom_empresa = request.POST["txtEmpresa"]
                unaEmpresa.correo = request.POST["txtCorreo"]
                unaEmpresa.slogan = request.POST["txtSlogan"]
                unaEmpresa.descripcion = request.POST["txtDescripcion"]
                unaEmpresa.dias_atencion = "Lunes - Domingo"
                unaEmpresa.politicas = request.POST["txtPoliticas"]
                unaEmpresa.direccion = request.POST["txtDireccion"]
                unaEmpresa.inicio_atencion = request.POST["txtHoraInicio"]
                unaEmpresa.fin_atencion = request.POST["txtHoraFin"]
                unaEmpresa.forma_venta = request.POST["txtFormaVenta"]
                unaEmpresa.forma_pago = request.POST["txtFormaPago"]
                unaEmpresa.costo_envio = float(request.POST["txtCostoEnvio"])
                unaActividad = activi_comerciales()
                unaActividad.id = int(request.POST["cmbActComerc"])
                unaEmpresa.activi_comercial = unaActividad
                # Se obtiene el directorio en donde se encuentran guardadas las imágenes
                imgPortada = unaEmpresa.ruta_foto.name.name
                imgPerfil = unaEmpresa.perfil_foto.name.name

                try:
                    unaEmpresa.ruta_foto = request.FILES["imgFoto"]
                    a, b = os.path.splitext(unaEmpresa.ruta_foto.name)
                    unaEmpresa.ruta_foto.name = "portada_empresa_" + \
                        str(unaEmpresa.id) + b
                    # Elimina la foto guardada en el directorio media del servidor
                    os.remove('media/'+imgPortada)
                except Exception as e:
                    pass

                try:
                    unaEmpresa.perfil_foto = request.FILES["imgFotoPerfil"]
                    a, b = os.path.splitext(unaEmpresa.perfil_foto.name)
                    unaEmpresa.perfil_foto.name = "perfil_empresa_" + \
                        str(unaEmpresa.id) + b
                    # Elimina la foto guardada en el directorio media del servidor
                    os.remove('media/'+imgPerfil)
                except Exception as e:
                    pass

                unaEmpresa.save()
                telefonos = telefo_empresas.objects.filter(empresa=unaEmpresa)
                for t in telefonos:
                    t.delete()
                cuentas = cuentas_bancarias.objects.filter(empresa=unaEmpresa)
                for c in cuentas:
                    c.delete()
                # Se obtiene la cantidad de números de teléfonos
                cantidadTelefo = int(request.POST["cantidadTelefo"])
                # Se obtienen y se guardan los números de teléfonos
                for i in range(cantidadTelefo):
                    unTelefono = telefo_empresas()
                    txttelefono = "txtTelefono" + str(i)
                    unTelefono.telefono = request.POST[txttelefono]
                    unTelefono.empresa = unaEmpresa
                    unTelefono.save()
                # Se obtiene la cantidad de cuentas bancarias
                cantidadCuentas = int(request.POST["cantidadCuentas"])
                # Se obtienen y se guardan las cuentas bancarias
                for i in range(cantidadCuentas):
                    unaCuenta = cuentas_bancarias()
                    entidad = "entidad" + str(i)
                    tipo_cuenta = "tipo_cuenta" + str(i)
                    numero = "numero" + str(i)
                    razon_social = "razon_social" + str(i)
                    unaCuenta.entidad = request.POST[entidad]
                    unaCuenta.tipo_cuenta = request.POST[tipo_cuenta]
                    unaCuenta.numero = request.POST[numero]
                    unaCuenta.razon_social = request.POST[razon_social]
                    unaCuenta.empresa = unaEmpresa
                    unaCuenta.save()

        return JsonResponse({"result": "1"})
    except Exception as e:
        return JsonResponse({"result": "0"})


# Vista que elimina fotos del carousel de la empresa
def vwElmFoto(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    try:
        unaEmpresa = empresas.objects.get(
            usuario_id=request.session["usuario"]["id"])
        idFoto = int(request.POST["id_foto"])
        foto = fotos_empresas.objects.get(id=idFoto)
        # Elimina la foto guardada en la carpeta media del servidor
        os.remove('media/'+foto.ruta_foto.name)
        # Elimina el directorio de la foto en la base de datos
        foto.delete()
        return JsonResponse({"result": "1"})
    except Exception as e:
        return JsonResponse({"result": "0"})


# Vista que guarda fotos del carousel de la empresa
def vwGrdFoto(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"] or request.session["usuario"]["rol_id"] == 1:
            return redirect("index")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    try:
        with transaction.atomic():
            unaEmpresa = empresas.objects.get(
                usuario_id=request.session["usuario"]["id"])
            unaFoto = fotos_empresas()
            unaFoto.empresa = unaEmpresa
            unaFoto.ruta_foto = request.FILES["imgFotoCarousel"]
            unaFoto.ruta_foto.name = "foto_carousel_empresa_" + \
                str(unaEmpresa.id) + ".jpeg"
            # Se guarda la foto en el servidor y se almacena el directorio de la foto en la base de datos
            unaFoto.save()
            return JsonResponse({"result": "1"})
    except Exception as e:
        return JsonResponse({"result": "0"})
