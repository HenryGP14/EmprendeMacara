from django.shortcuts import render
from django.http import JsonResponse, Http404
from Modelos.models import activi_comerciales, empresas, telefo_empresas, usuarios, rol
from django.db import transaction

# Vista que renderiza la plantilla de solicitar cuenta
def vwTplSolicitar(request):
    actividadesCom = activi_comerciales.objects.all()
    return render(request, "tplSolicitarCuenta.html", {"actividadesCom": actividadesCom})

# Vista que guarda una solicitud
def vwGrdSolicit(request):
    try:
        with transaction.atomic():
            # Se crea un objeto rol y su id será el 2, por defecto en la BD es un emprendedor
            unRol = rol()
            unRol.id = 2
            # Se verifica que no exista un usuario repetido            
            existeUsuario = usuarios.objects.filter(correo=request.POST['txtUsuario'])
            if(len(existeUsuario)):
                return JsonResponse({"result": 'El usuario ya se encuentra registrado, por favor ingrese otro usuario'})
            else:
                # Se verifica que no exista otra empresa con el mismo correo
                correoEmpresa = empresas.objects.filter(correo=request.POST['txtCorreo'])
                if(len(correoEmpresa)):
                    return JsonResponse({"result": 'El correo de la empresa ya encuentra registrado, por favor ingrese otro correo'})
                else:
                    unUsuario = usuarios()
                    unUsuario.correo = request.POST['txtUsuario']
                    unUsuario.nom_usuario = request.POST['txtGerente']
                    unUsuario.credenciales = request.POST['txtContrasenia']
                    unUsuario.rol = unRol
                    # El usuario tendrá un estado con valor de False hasta que se apruebe su solicitud
                    unUsuario.estado = False
                    unUsuario.save()
                    unaEmpresa = empresas()
                    unaEmpresa.usuario = unUsuario
                    unaEmpresa.gerente = request.POST['txtGerente']
                    unaEmpresa.ruc = request.POST['txtRuc']
                    unaEmpresa.nom_empresa = request.POST['txtEmpresa']
                    unaEmpresa.correo = request.POST['txtCorreo']
                    unaEmpresa.slogan = request.POST['txtSlogan']
                    unaEmpresa.dias_atencion = "Lunes - Domingo"
                    unaEmpresa.politicas = request.POST['txtPoliticas']
                    unaEmpresa.direccion = request.POST['txtDireccion']
                    unaEmpresa.inicio_atencion = request.POST['txtHoraInicio']
                    unaEmpresa.fin_atencion = request.POST['txtHoraFin']
                    # La empresa tendrá un estado con valor de Solicitante hasta que se apruebe su solicitud
                    unaEmpresa.estado = "Solicitante"
                    unaActividad = activi_comerciales()
                    unaActividad.id = int(request.POST['cmbActComerc'])
                    unaEmpresa.activi_comercial = unaActividad
                    unaEmpresa.save()
                    # Se obtiene la cantidad de números de teléfono ingresados
                    cantidadTelefo = int(request.POST['cantidadTelefo'])
                    # Se obtienen y se guardan los números de teléfonos
                    for i in range(cantidadTelefo):
                        unTelefono = telefo_empresas()
                        txttelefono = "txtTelefono"+str(i)
                        unTelefono.telefono = request.POST[txttelefono]
                        unTelefono.empresa = unaEmpresa
                        unTelefono.save()
          
        return JsonResponse({"result": '1'})
    except Exception as e:
        return JsonResponse({"result": '0'})

