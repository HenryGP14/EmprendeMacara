from django.db import models
from fernet_fields import EncryptedTextField

# Create your models here.


class rol(models.Model):
    nombre = models.CharField(max_length=20, unique=True)


class usuarios(models.Model):
    # un objeto de tipo rol que tiene el id de un rol
    nom_usuario = models.CharField(max_length=50)
    rol = models.ForeignKey(rol, on_delete=models.PROTECT, related_name="usuarios")
    correo = models.EmailField(max_length=75, unique=True)
    credenciales = EncryptedTextField()
    # media/Perfiles
    ruta_foto = models.ImageField(upload_to="Perfiles", null=True, blank=False)
    # True= usuario habilitado que puede iniciar sesión, False= deshabilitado
    estado = models.BooleanField()
    correo_verificado = models.BooleanField(default=True)


class activi_comerciales(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    # media/ActividadC
    ruta_foto = models.ImageField(upload_to="ActividadC", null=True, blank=False)


class empresas(models.Model):
    # un objeto de tipo ActiviComercial que tiene el id de un Actividad Comercial
    activi_comercial = models.ForeignKey(activi_comerciales, on_delete=models.PROTECT, related_name="empresas")
    # un objeto de tipo Usuario que tiene el id de un usuario
    usuario = models.OneToOneField(usuarios, on_delete=models.PROTECT, related_name="empresa")
    gerente = models.CharField(max_length=50)
    nom_empresa = models.CharField(max_length=50, unique=True)
    ruc = models.CharField(max_length=13)
    slogan = models.TextField(max_length=600)
    correo = models.EmailField(max_length=75)
    direccion = models.TextField(max_length=150)
    inicio_atencion = models.TimeField()
    fin_atencion = models.TimeField()
    dias_atencion = models.CharField(max_length=25, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    forma_pago = models.TextField(null=True, blank=True)
    forma_venta = models.TextField(null=True, blank=True)
    politicas = models.TextField(max_length=600)
    costo_envio = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True)
    # Estados de una empresa
    # Habilitada= empresa visible para los clientes, Deshabilitada= empresa invisible para los clientes,
    # Solicitante = empresa en proceso de aprobación por el administrador
    estado = models.CharField(max_length=13)
    perfil_foto = models.ImageField(upload_to="Perfiles", null=True, blank=True)
    ruta_foto = models.ImageField(upload_to="Portadas", null=True, blank=True)  # media/Portadas


class telefo_empresas(models.Model):
    # un objeto de tipo Empresa que tiene el id de la empresa
    empresa = models.ForeignKey(empresas, on_delete=models.PROTECT, related_name="telefonos")
    telefono = models.CharField(max_length=10)


class fotos_empresas(models.Model):
    # un objeto de tipo Empresa que tiene el id de la empresa
    empresa = models.ForeignKey(empresas, on_delete=models.PROTECT, related_name="fotos_empresa")
    # Carrucel/nombre.jpg
    ruta_foto = models.ImageField(upload_to="Carrusel", null=True, blank=False)


class cuentas_bancarias(models.Model):
    # un objeto de tipo Empresa que tiene el id de la empresa
    empresa = models.ForeignKey(empresas, on_delete=models.PROTECT, related_name="cuentas_bancarias")
    # entidad= banco pichincha
    entidad = models.CharField(max_length=40)
    # tipocuenta = cuenta de ahorros
    tipo_cuenta = models.CharField(max_length=30)
    # numero= 0000584848
    numero = models.CharField(max_length=10)
    # razonsocial= propietario de la cuenta
    razon_social = models.CharField(max_length=50)


class servicios(models.Model):
    empresa = models.ForeignKey(empresas, on_delete=models.PROTECT, related_name="servicios")
    nombre = models.TextField()
    # Entrega a domicilio
    # Se entrega a domicilio a cualquier lugar de la localidad
    descripcion = models.TextField()
    # media/Productos_Servicios
    ruta_foto = models.ImageField(upload_to="Productos_Servicios", null=True, blank=False)
    visible = models.BooleanField()
    Eliminado = models.BooleanField(default=False)


class productos(models.Model):
    empresa = models.ForeignKey(empresas, on_delete=models.PROTECT, related_name="productos")
    nombre = models.TextField()
    # Helado de cono
    # Helados de cono sabor a chocolate, fresa, etc..
    descripcion = models.TextField()
    # 15
    cantidad = models.IntegerField()
    # 1.5
    precio_unitario = models.DecimalField(max_digits=6, decimal_places=2)
    # media/Productos_Servicios
    ruta_foto = models.ImageField(upload_to="Productos_Servicios", null=True, blank=False)
    visible = models.BooleanField()
    Eliminado = models.BooleanField(default=False)

class ventas(models.Model):
    secuencial = models.CharField(max_length=11, unique=True)
    empresa = models.ForeignKey(empresas, on_delete=models.PROTECT, related_name="ventas")
    fecha = models.DateField()
    cliente = models.CharField(max_length=50)
    cedula = models.CharField(max_length=10)
    celular = models.CharField(max_length=10)
    correo = models.EmailField(max_length=75)
    direccion_entrega = models.TextField()
    tipo_de_pago = models.CharField(max_length=22, null=False, blank=True)
    estado = models.CharField(max_length=22, null=False, blank=True)
    # Entregado-Pendiente-Anulado-Enviado


class detalles_venta(models.Model):
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=6, decimal_places=2)
    precio_sub_total = models.DecimalField(max_digits=6, decimal_places=2)
    precio_envio = models.DecimalField(max_digits=6, decimal_places=2)
    monto_depositado = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    entidad_bancaria = models.CharField(max_length=40, blank=True, null=True)
    num_documento = models.CharField(max_length=10, blank=True, null=True)
    ruta_foto = models.ImageField(upload_to="Depositos", blank=True, null=True)
    venta = models.ForeignKey(ventas, on_delete=models.PROTECT, related_name="detalles_venta")
    producto = models.ForeignKey(productos, on_delete=models.PROTECT, related_name="detalles_venta")
