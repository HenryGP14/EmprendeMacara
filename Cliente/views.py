from django.shortcuts import (
    render,
    redirect,
)
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse

from Modelos.models import (
    usuarios,
    clientes,
    productos,
    carritos,
    empresas,
    cuentas_bancarias,
    ventas,
    detalles_venta,
)

from Cliente.carrito import Carrito
from Global.usuario import Usuario
from datetime import datetime

import os

# Vista que permite reguistrar un cliente y guardar sus datos en la base de datos
def vwRegCliente(request):
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

    # Guardar datos del cliente por medio de transaciones
    with transaction.atomic():
        try:
            usuario = usuarios.objects.create(
                nom_usuario=request.POST["txtNombre"],
                correo=request.POST["txtCorreo"],
                credenciales=request.POST["txtCredenciales"],
                ruta_foto="",
                estado=True,
                rol_id=1,
            )
            clientes.objects.create(
                nombres=request.POST["txtNombre"],
                cedula=request.POST["txtCedula"],
                direccion=request.POST["txtDireccion"],
                telefono=request.POST["txtCelular"],
                usuario_id=usuario.id,
            )
        except:
            messages.error(request, "!Ups¡ Tuvimos problemas en registrarte inténtalo de nuevo")
            return JsonResponse({"redirect": ""})
    messages.success(request, "Felicitaciones. Tu usuario se registro correctamente, inicia sesión para verificar")
    return JsonResponse({"redirect": "login"})


# Vista que retorna el template de las configuraciones
def vwTplConfiguracion(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"]:
            messages.info(
                request,
                "Debes iniciar sessión",
            )
            return redirect("login")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    return render(request, "tplConfiguraciones.html")


# Vita que permite guardar la nueva contraseña del usuario cliente
def vwGrdCredenciales(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"]:
            messages.info(request, "Debes iniciar sessión")
            return redirect("login")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass
    try:
        usuario = usuarios.objects.get(pk=request.session["usuario"]["id"])
        # Identifica si la contraseña antigua coinciden
        if usuario.credenciales == request.POST["txtCredenciales"]:
            usuario.credenciales = request.POST["txtCredenciales_new"]
            usuario.save()
        else:
            messages.error(request, "!Ups¡ La contraseña antigua que ingresaste no es la correcta")
            return JsonResponse({"redirect": "configuraciones"})
    except:
        messages.error(request, "!Ups¡ Tuvimos problemas al cambiar la contraseña")
        return JsonResponse({"redirect": "configuraciones"})
    messages.success(request, "Felicitaciones. Tu contraseña se cambio correctamente, inicia sesión para seguir con tus compras")
    return JsonResponse({"redirect": "\logout"})


# Vista que permite guardar el nuevo perfil del usuario cliente
def vwGrdPerfil(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"]:
            messages.info(request, "Debes iniciar sessión")
            return redirect("login")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass
    try:
        usuario = usuarios.objects.get(pk=request.session["usuario"]["id"])
        usuario.ruta_foto = request.FILES.get("image")

        # Obtinene el nombre de la foto en old_nom_foto y el tipo de archivo en tipo_foto
        (
            old_nom_foto,
            tipo_foto,
        ) = os.path.splitext(usuario.ruta_foto.name)

        # Guarda el nombre de la foto de la siguiente manera Nombre_usuarioid.tipo_archivo
        # También también reemplazando las letras que tienen tildes
        new_nom_foto = (
            request.session["usuario"]["nombre"]
            .replace(" ", "_")
            .replace("á", "a")
            .replace("Á", "A")
            .replace("é", "e")
            .replace("É", "E")
            .replace("í", "i")
            .replace("Í", "I")
            .replace("ó", "o")
            .replace("Ó", "O")
            .replace("ú", "u")
            .replace("Ú", "U")
            .replace("ñ", "n")
            .replace("Ñ", "N")
        )
        # Cambia el nombre de la imagen subida
        usuario.ruta_foto.name = new_nom_foto + "_" + str(request.session["usuario"]["id"]) + tipo_foto
        try:
            if request.session["usuario"]["perfil"]:
                os.remove(request.session["usuario"]["perfil"][1:])
        except:
            pass
        # Guarda y edita la imagen en el usuario session
        usuario.save()
        user_session.edit_perfil(usuario.ruta_foto)
    except Exception as e:
        messages.error(request, "Error al subir la imagen, a escogido un archivo con formato incorrecto")
        return JsonResponse({"redirect": ""})
    messages.success(request, "Felicitaciones. foto de perfil se cambio correctamente")
    return JsonResponse({"redirect": ""})


# Vista que permite guardar el nuevo nombre del usuario cliente
def vwGrdNombre(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"]:
            messages.info(request, "Debes iniciar sessión")
            return redirect("login")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass
    try:
        usuario = usuarios.objects.get(pk=request.session["usuario"]["id"])
        nom_new_usuario = request.POST["user_nombre"]

        # Valida que el nombre no tenga espacio a la izquierda y derecha
        usuario.nom_usuario = nom_new_usuario.strip()

        # Guarda y modifica el nombre de usuario en la variable session
        usuario.save()
        user_session.edit_nombre(usuario.nom_usuario)
    except Exception as e:
        messages.error(request, e)
        return JsonResponse({"redirect": "configuraciones"})
    messages.success(request, "Felicitaciones. el nombre se cambio correctamente")
    return JsonResponse({"redirect": ""})


# Vista que permite ver el contenido del carrito, es decir, los productos que he guardado en el carrito
def vwTplCarrito(request):
    user_session = Usuario(request)
    cart_session = Carrito(request)
    try:
        if not request.session["usuario"]:
            messages.info(request, "Debes iniciar sessión para ver los productos que tienes en el carrito")
            return redirect("login")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass
    return render(request, "tplCarrito.html")


# Vista que permita agredar un nuevo prducto al carrito, si ya existe solo aumenta un elemento
def vwAggPrCart(request, producto_id):
    user_session = Usuario(request)
    cart_session = Carrito(request)
    try:
        if not request.session["usuario"]:
            messages.info(request, "Debes iniciar sessión para añadir el producto al carrito")
            return redirect("login")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    # Obtiene el producto y lo agrega al carrito
    producto = productos.objects.get(pk=producto_id)
    cart_session.add(producto)
    messages.success(request, "Su producto se ha guardado al carrito")
    return redirect("pr_sr_negocio", producto.empresa.id)


# Vista para eliminar todos los carritos en session
def vwClsCarrito(request):
    user_session = Usuario(request)
    cart_session = Carrito(request)
    try:
        if not request.session["usuario"]:
            messages.info(request, "Debes iniciar sessión para añadir el producto al carrito")
            return redirect("login")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    # Elimina todo los productos del carrito
    cart_session.clear()
    messages.success(request, "Has eliminado todo los produtos del carrito")
    return redirect("carrito")


# Vista que permite incrementar el número de productos en el carrito
def vwIncrementarPrCart(request):
    # Incrementa la cantidad de productos en el carrito
    cart_session = Carrito(request)
    producto = productos.objects.get(pk=request.POST["producto_id"])
    cart_session.add(producto)
    return JsonResponse({"Guardado": True})


# Vista que permite decrementar el número de productos en el carrito
def vwDecrementarPrCart(request):
    # Decrementa la cantidad de productos en el carrito
    cart_session = Carrito(request)
    producto = productos.objects.get(pk=request.POST["producto_id"])
    cart_session.decrement(producto)
    return JsonResponse({"Guardado": True})


# Vista que permite eliminar un producto que estaba en el carrito, también lo elimina de la base de datos
def vwElmProductoCart(request, producto_id):
    user_session = Usuario(request)
    cart_session = Carrito(request)
    try:
        if not request.session["usuario"]:
            messages.info(request, "Debes iniciar sessión para añadir el producto al carrito")
            return redirect("login")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass
    producto = productos.objects.get(pk=producto_id)
    carrito = carritos.objects.filter(
        usuario_id=request.session["usuario"]["id"],
        producto_id=producto_id,
    )

    # Elimina un producto del carrito y de la base de datos Carrito
    carrito.delete()
    cart_session.remove(producto)
    messages.success(request, "El producto " + producto.nombre + "se elimino de tu carrito")
    return redirect("carrito")


# Vista que retorna el html de los pedios, listando los pedidos que ha compado
def vwTplPedidos(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"]:
            messages.info(request, "Debes iniciar sessión para visualizar esta opción")
            return redirect("login")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass
    usuario = usuarios.objects.get(pk=request.session["usuario"]["id"])
    cliente_id = usuario.cliente.id
    pedidos = ventas.objects.filter(cliente_id=cliente_id)
    return render(request, "tplPedidos.html", {"pedidos": pedidos})


# Vista que permite obtener el detalle del pedido comprado
def vwObtenerDtPed(request):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"]:
            messages.info(request, "Debes iniciar sessión para visualizar esta opción")
            return redirect("login")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    # Obtengo los detalles del pedido comprado
    detalles = ventas.objects.get(pk=request.POST["pedido_id"])
    datos = {
        "prod_nombre": detalles.detalles_venta.all()[0].producto.nombre,
        "prod_descripcion": detalles.detalles_venta.all()[0].producto.descripcion if detalles.detalles_venta.all()[0].producto.descripcion else "El poducto no cuenta con una descripción",
        "prod_cantidad": detalles.detalles_venta.all()[0].cantidad,
        "prod_precio": detalles.detalles_venta.all()[0].precio_unitario,
        "prec_envio": detalles.detalles_venta.all()[0].precio_envio,
        "prod_estado": detalles.estado,
        "prod_img": detalles.detalles_venta.all()[0].producto.ruta_foto.url if detalles.detalles_venta.all()[0].producto.ruta_foto else False,
        "fecha": detalles.fecha,
        "nom_banco": detalles.detalles_venta.all()[0].entidad_bancaria if detalles.detalles_venta.all()[0].entidad_bancaria else False,
        "num_deposito": detalles.detalles_venta.all()[0].num_documento,
        "img_deposito": detalles.detalles_venta.all()[0].ruta_foto.url if detalles.detalles_venta.all()[0].ruta_foto else False,
    }
    return JsonResponse({"datos": datos})


# Vista que retorna el html de detalle de facturación, es decir, culminar la compra
def vwTplDtFactura(request, producto_id):
    user_session = Usuario(request)
    try:
        if not request.session["usuario"]:
            messages.info(request, "Debes iniciar sessión para añadir el producto al carrito")
            return redirect("login")
        elif request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    usuario = usuarios.objects.get(pk=request.session["usuario"]["id"])
    producto = request.session["carrito"][str(producto_id)]
    cliente = clientes.objects.filter(usuario_id=request.session["usuario"]["id"])

    # Obtener cuentas bancarias
    producto_obj = productos.objects.get(pk=producto["producto_id"])
    cuenta_banc = cuentas_bancarias.objects.filter(empresa_id=producto_obj.empresa)

    subtotal = int(producto["cantidad"]) * float(producto["precio"])
    costo_envio = producto_obj.empresa.costo_envio
    total = float(subtotal) + float(costo_envio)

    # Guardar los necesarios para enviarlos al html
    datos = {
        "nombre": usuario.nom_usuario,
        "correo": usuario.correo,
        "direccion": cliente[0].direccion,
        "telefono": cliente[0].telefono,
        "id_producto": producto_obj.id,
        "nombre_producto": producto["nom_producto"],
        "cantidad": producto["cantidad"],
        "precio": str(producto["precio"]).replace(".", ","),
        "subtotal": str("{0:.2f}".format(subtotal).replace(".", ",")),
        "costo_envio": str("{0:.2f}".format(costo_envio).replace(".", ",")),
        "total": str("{0:.2f}".format(total).replace(".", ",")),
        "cuentas_bancarias": cuenta_banc,
    }

    return render(request, "tplDtFactura.html", context={"datos": datos})


# Vista que permite registrar el pedido a la base de datos
def vwRegPedido(request):
    nombres = request.POST["nombres"]
    email = request.POST["email"]
    direccion = request.POST["direccion"]
    celular = request.POST["celular"]

    cliente = clientes.objects.filter(usuario_id=request.session["usuario"]["id"])
    producto_obj = productos.objects.get(pk=request.POST["id_producto"])

    # Tabla ventas
    venta = ventas()
    venta.fecha = datetime.now()
    venta.direccion_entrega = direccion
    venta.celular = request.POST["celular"]
    venta.estado = "Pendiente"
    venta.cliente_id = cliente[0].id
    venta.empresa_id = producto_obj.empresa_id
    venta.tipo_de_pago = request.POST["metodo_pago"]
    venta.save()

    # tabla detalle de venta
    detalle_venta = detalles_venta()
    detalle_venta.venta_id = venta.id
    detalle_venta.producto_id = producto_obj.id
    detalle_venta.cantidad = int(request.POST["cantidad"])
    detalle_venta.precio_unitario = producto_obj.precio_unitario
    # Sacar el sub total del producto, sin el costo de envio
    precio_subt_producto = float(str(request.POST["cantidad"]).replace(",", ".")) * float(producto_obj.precio_unitario)
    detalle_venta.precio_sub_total = precio_subt_producto
    detalle_venta.precio_envio = producto_obj.empresa.costo_envio

    if request.POST["metodo_pago"] == "Depósito":
        detalle_venta.monto_depositado = float(str(request.POST["valor-deposito"]).replace(",", "."))
        detalle_venta.entidad_bancaria = request.POST["entidad-bancaria"]
        detalle_venta.num_documento = request.POST["num-documento"]
        detalle_venta.ruta_foto = request.FILES["img-deposito"]
        hoy = datetime.now()
        exten = str(detalle_venta.ruta_foto.name).split(".")
        detalle_venta.ruta_foto.name = "deposito_" + str(hoy.strftime("%y-%m-%d %H.%M.%S")) + "." + exten[-1]

    detalle_venta.save()

    cart = carritos.objects.filter(
        usuario_id=request.session["usuario"]["id"],
        producto_id=producto_obj.id,
    )
    cart.delete()
    carrito = Carrito(request)
    carrito.remove(producto_obj)

    return redirect("index")
