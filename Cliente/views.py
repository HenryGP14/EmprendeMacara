from django.shortcuts import (
    render,
    redirect,
)
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse

from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from Modelos.models import (
    usuarios,
    productos,
    empresas,
    cuentas_bancarias,
    ventas,
    detalles_venta,
)

from Cliente.carrito import Carrito
from Global.usuario import Usuario
from Global.correo import Correo
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

# Vista que retorna el html de detalle de facturación, es decir, culminar la compra
def vwTplDtFactura(request, producto_id):
    user_session = Usuario(request)
    try:
        if request.session["usuario"]["rol_id"] == 2:
            return redirect("controlNegocio")
        elif request.session["usuario"]["rol_id"] == 3:
            return redirect("admin-web")
    except:
        pass

    producto = request.session["carrito"][str(producto_id)]

    # Obtener cuentas bancarias
    producto_obj = productos.objects.get(pk=producto["producto_id"])
    cuenta_banc = cuentas_bancarias.objects.filter(empresa_id=producto_obj.empresa)

    subtotal = int(producto["cantidad"]) * float(producto["precio"])
    costo_envio = producto_obj.empresa.costo_envio
    total = float(subtotal) + float(costo_envio)

    # Guardar los necesarios para enviarlos al html
    datos = {
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
    with transaction.atomic():
        producto_obj = productos.objects.get(pk=request.POST["id_producto"])

        # Tabla ventas
        venta = ventas()
        venta.fecha = datetime.now()
        venta.direccion_entrega = request.POST["direccion"]
        venta.cliente = request.POST["nombres"]
        venta.cedula = request.POST["cedula"]
        venta.celular = request.POST["celular"]
        venta.correo = request.POST["email"]
        venta.estado = "Pendiente"

        venta.empresa_id = producto_obj.empresa_id
        empresa = empresas.objects.get(id=venta.empresa_id)
        venta.tipo_de_pago = request.POST["metodo_pago"]
        venta.save()

        # tabla detalle de venta
        detalle_venta = detalles_venta()
        detalle_venta.venta_id = venta.id
        detalle_venta.producto = producto_obj
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

        unCorreo = Correo(request)
        context = {"tipoUsuario": "empresa", "venta": venta, "detalle_venta": detalle_venta, "costoEnvio": str("{0:.2f}".format(producto_obj.empresa.costo_envio)).replace(".", ","),"total": ("{0:.2f}".format(float(detalle_venta.precio_sub_total) + float(detalle_venta.precio_envio))).replace(".", ",")}
        unUsuarioAdmin = usuarios.objects.filter(rol_id=3).first()
        if(unCorreo.send(unUsuarioAdmin, empresa.correo, "Facturación del pedido - Emprendimientos Macará", "factura-correo.html", context)):
            unCorreo = Correo(request)
            context = {"tipoUsuario": "cliente", "venta": venta, "detalle_venta": detalle_venta, "costoEnvio": str("{0:.2f}".format(producto_obj.empresa.costo_envio)).replace(".", ","),"total": ("{0:.2f}".format(float(detalle_venta.precio_sub_total) + float(detalle_venta.precio_envio))).replace(".", ",")}
            unUsuarioAdmin = usuarios.objects.filter(rol_id=3).first()
            unCorreo.send(unUsuarioAdmin, venta.correo, "Facturación del pedido - Emprendimientos Macará", "factura-correo.html", context)

        carrito = Carrito(request)
        carrito.remove(producto_obj)

        return redirect("index")

