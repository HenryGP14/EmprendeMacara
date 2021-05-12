class Carrito:

    # Creación de carrito en variable session
    def __init__(self, request):
        # Inicializar carrito si no existe
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}
        # Esta linea permite decirle a django que elimine las sessión del carrito cuando cierra el navegador
        request.session.set_expiry(0)
        # Fin
        self.carrito = carrito

    def add(self, producto):
        # Guardar producto en el carrito si no existe
        if str(producto.id) not in self.carrito.keys():
            self.carrito[producto.id] = {
                "producto_id": producto.id,
                "nom_producto": producto.nombre,
                "descripcion": producto.descripcion,
                "cantidad": 1,
                "precio": str(producto.precio_unitario),
                "foto": producto.ruta_foto.url if producto.ruta_foto else False,
                "empresa": producto.empresa.nom_empresa,
            }
        # Si existe el producto se suma un elemento a cantidad
        else:
            for key, value in self.carrito.items():
                if key == str(producto.id):
                    value["cantidad"] += 1
                    break
        self.save()

    def add_cart(self, cart):
        # Guardar producto en el carrito cuando el cliente inicia sesión
        if str(cart.producto_id) not in self.carrito.keys():
            self.carrito[cart.producto_id] = {
                "producto_id": cart.producto_id,
                "nom_producto": cart.producto.nombre,
                "descripcion": cart.producto.descripcion,
                "cantidad": cart.cantidad,
                "precio": str(cart.producto.precio_unitario),
                "foto": cart.producto.ruta_foto.url if cart.producto.ruta_foto else False,
                "empresa": cart.producto.empresa.nom_empresa,
            }
        else:
            for key, value in self.carrito.items():
                if key == str(cart.producto.id):
                    value["cantidad"] += 1
                    break
        self.save()

    def save(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def remove(self, producto):
        # Eliminar el producto en el carrito
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.save()

    def decrement(self, producto):
        # Decrementar la cantidad de producto
        for key, value in self.carrito.items():
            if key == str(producto.id):
                value["cantidad"] -= 1
                if value["cantidad"] < 1:
                    self.remove()
                else:
                    self.save()
                break

    def clear(self):
        self.session["carrito"] = {}
        self.session.modified = True
