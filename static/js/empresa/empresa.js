//Evento click para añadir un teléfono
$("#btnAddTelefono").click(function () {
    txttelefono = $("#txttelefono").val();
    if (txttelefono.length == 7 | txttelefono.length == 10) {
        if ($("#tableTelefono-body tr").length < 3) {
            // Verifica que no existan números repetidos
            if (validaNumRepe(txttelefono)) {
                row = '<tr class="numero" id="' + txttelefono + '">' +
                    '<td> ' + txttelefono + ' </td>' +
                    '<td><a class="btn btn-xs btn-danger text-white" href="javascript:deleteTelefo(' + "'" + txttelefono + "'" + ');"><i class="fa fa-trash" aria-hidden="true"></i></a></td>' +
                    '</tr>';
                document.querySelector("#txttelefono").value = ""
                $("#tableTelefonos tbody").prepend(row);
            }
            else {
                Swal.fire({
                    icon: 'error',
                    text: 'El número de teléfono ya existe, por favor ingrese un número diferente'
                })
            }
        }
        else {
            Swal.fire({
                icon: 'info',
                text: 'Ya completó el número máximo de ingreso de números de teléfonos'
            })
        }
    } else {
        Swal.fire({
            icon: 'warning',
            text: 'El número de teléfono debe tener 7 o 10 dígitos'
        })
    }
});

//Función que verifica que no existan número de teléfonos repetidos
function validaNumRepe(telefono) {
    var bandera = true
    $('.numero').each(function () {
        if (telefono == $(this).attr('id')) {
            bandera = false;
        }
    });
    return bandera;
}

// Función que muestra un mensaje de confirmación para la eliminación de un número de teléfono
function deleteTelefo(txttelefono) {
    swal({
        text: "¿Desea eliminar el número de teléfono " + txttelefono + "?",
        icon: "info",
        buttons: ['NO', 'YES'],
      dangerMode: true
    }).then((value) => {
        // Si es true, significa que respondió SI
        if (value == true) {
            $("#" + txttelefono).remove();
            Swal.fire({
                icon: 'success',
                text: 'Número de teléfono eliminado'
            })
        }
    });
}

// Evento submit que se ejecuta cuando el usuario da click en Guardar
$(document).ready(function () {
    $("#formSolicitar").submit(function (e) {
        e.preventDefault();
        var parametros = new FormData($(this)[0]);
        if (validarContraseña("#txtContrasenia", "#txtConfirContra")) {
            document.querySelector("#btnEnviar").setAttribute("disabled", false);
            document.body.style.cursor = 'wait';
            var txtRuc = $("#txtRuc").val();
            if (txtRuc.length == 10 | txtRuc.length == 13) {
                if ($('#tableTelefono-body tr').length > 0) {
                    var numTelefono = 0
                    $('.numero').each(function () {
                        parametros.append("txtTelefono" + numTelefono, $(this).attr('id'));
                        numTelefono++;
                    });
                    parametros.append("cantidadTelefo", numTelefono);
                    $.ajax({
                        url: '/empresa/enviar-solicitud/',
                        type: 'POST',
                        data: parametros,
                        dataType: 'json',
                        cache: false,
                        contentType: false,
                        processData: false
                    }).done(function (data) {
                        document.body.style.cursor = 'default';
                        // Si el resultado es 1, la transacción fue realizada correctamente
                        if (data.result == '1') {
                            $('#solicitud_enviada').modal('show');
                        } else if (data.result == '0') {
                            document.querySelector("#btnEnviar").removeAttribute("disabled")
                            Swal.fire({
                                icon: 'error',
                                text: 'Error al enviar la solicitud, por favor intente nuevamente'
                            })
                        } else {
                            document.querySelector("#btnEnviar").removeAttribute("disabled")
                            Swal.fire({
                                icon: 'error',
                                text: data.result
                            })
                        }
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        document.body.style.cursor = 'default';
                        document.querySelector("#btnEnviar").removeAttribute("disabled")
                        Swal.fire({
                            icon: 'error',
                            text: 'Error al enviar la solicitud, por favor intente nuevamente'
                        })
                    }).always(function (data) {
                    });
                }
                else {
                    document.body.style.cursor = 'default';
                    document.querySelector("#btnEnviar").removeAttribute("disabled")
                    Swal.fire({
                        icon: 'warning',
                        text: 'Es obligatorio ingresar al menos un número de teléfono'
                    })
                }
            }
            else {
                document.body.style.cursor = 'default';
                document.querySelector("#btnEnviar").removeAttribute("disabled")
                Swal.fire({
                    icon: 'error',
                    text: 'El número de ruc o cédula es inválido, debe tener una longitud de 10 o 13 dígitos'
                })
            }
        }
    });
});
