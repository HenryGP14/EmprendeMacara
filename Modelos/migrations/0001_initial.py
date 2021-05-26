# Generated by Django 3.0.8 on 2021-05-26 18:21

from django.db import migrations, models
import django.db.models.deletion
import fernet_fields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='activi_comerciales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('ruta_foto', models.ImageField(null=True, upload_to='ActividadC')),
            ],
        ),
        migrations.CreateModel(
            name='empresas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gerente', models.CharField(max_length=50)),
                ('nom_empresa', models.CharField(max_length=50, unique=True)),
                ('ruc', models.CharField(max_length=13)),
                ('slogan', models.TextField(max_length=600)),
                ('correo', models.EmailField(max_length=75)),
                ('direccion', models.TextField(max_length=150)),
                ('inicio_atencion', models.TimeField()),
                ('fin_atencion', models.TimeField()),
                ('dias_atencion', models.CharField(blank=True, max_length=25, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('forma_pago', models.TextField(blank=True, null=True)),
                ('forma_venta', models.TextField(blank=True, null=True)),
                ('politicas', models.TextField(max_length=600)),
                ('costo_envio', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True)),
                ('estado', models.CharField(max_length=13)),
                ('perfil_foto', models.ImageField(blank=True, null=True, upload_to='Perfiles')),
                ('ruta_foto', models.ImageField(blank=True, null=True, upload_to='Portadas')),
                ('activi_comercial', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='empresas', to='Modelos.activi_comerciales')),
            ],
        ),
        migrations.CreateModel(
            name='rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ventas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secuencial', models.CharField(max_length=11, unique=True)),
                ('fecha', models.DateField()),
                ('cliente', models.CharField(max_length=50)),
                ('cedula', models.CharField(max_length=10)),
                ('celular', models.CharField(max_length=10)),
                ('correo', models.EmailField(max_length=75)),
                ('direccion_entrega', models.TextField()),
                ('tipo_de_pago', models.CharField(blank=True, max_length=22)),
                ('estado', models.CharField(blank=True, max_length=22)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ventas', to='Modelos.empresas')),
            ],
        ),
        migrations.CreateModel(
            name='usuarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_usuario', models.CharField(max_length=50)),
                ('correo', models.EmailField(max_length=75, unique=True)),
                ('credenciales', fernet_fields.fields.EncryptedTextField()),
                ('ruta_foto', models.ImageField(null=True, upload_to='Perfiles')),
                ('estado', models.BooleanField()),
                ('correo_verificado', models.BooleanField(default=True)),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='usuarios', to='Modelos.rol')),
            ],
        ),
        migrations.CreateModel(
            name='telefo_empresas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.CharField(max_length=10)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='telefonos', to='Modelos.empresas')),
            ],
        ),
        migrations.CreateModel(
            name='servicios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField()),
                ('descripcion', models.TextField()),
                ('ruta_foto', models.ImageField(null=True, upload_to='Productos_Servicios')),
                ('visible', models.BooleanField()),
                ('eliminado', models.BooleanField(default=False)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='servicios', to='Modelos.empresas')),
            ],
        ),
        migrations.CreateModel(
            name='productos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField()),
                ('descripcion', models.TextField()),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=6)),
                ('ruta_foto', models.ImageField(null=True, upload_to='Productos_Servicios')),
                ('visible', models.BooleanField()),
                ('eliminado', models.BooleanField(default=False)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='productos', to='Modelos.empresas')),
            ],
        ),
        migrations.CreateModel(
            name='fotos_empresas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ruta_foto', models.ImageField(null=True, upload_to='Carrusel')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fotos_empresa', to='Modelos.empresas')),
            ],
        ),
        migrations.AddField(
            model_name='empresas',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='empresa', to='Modelos.usuarios'),
        ),
        migrations.CreateModel(
            name='detalles_venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=6)),
                ('precio_sub_total', models.DecimalField(decimal_places=2, max_digits=6)),
                ('precio_envio', models.DecimalField(decimal_places=2, max_digits=6)),
                ('monto_depositado', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('entidad_bancaria', models.CharField(blank=True, max_length=40, null=True)),
                ('num_documento', models.CharField(blank=True, max_length=10, null=True)),
                ('ruta_foto', models.ImageField(blank=True, null=True, upload_to='Depositos')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='detalles_venta', to='Modelos.productos')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='detalles_venta', to='Modelos.ventas')),
            ],
        ),
        migrations.CreateModel(
            name='cuentas_bancarias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entidad', models.CharField(max_length=40)),
                ('tipo_cuenta', models.CharField(max_length=30)),
                ('numero', models.CharField(max_length=10)),
                ('razon_social', models.CharField(max_length=50)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cuentas_bancarias', to='Modelos.empresas')),
            ],
        ),
    ]
