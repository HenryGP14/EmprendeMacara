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

# Vista que permite ver el contenido del carrito, es decir, los productos que he guardado en el carrito
def vwTplCarrito(request):
    cart_session = Carrito(request)
    try:
        if request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass
    return render(request, "tplCarrito.html")


# Vista que permita agredar un nuevo prducto al carrito, si ya existe solo aumenta un elemento
def vwAggPrCart(request, producto_id):
    cart_session = Carrito(request)
    try:
        if request.session["usuario"]["rol_id"] == 2:
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
    cart_session = Carrito(request)
    try:
        if request.session["usuario"]["rol_id"] == 2:
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
    cart_session = Carrito(request)
    try:
        if request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass
    producto = productos.objects.get(pk=producto_id)
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
