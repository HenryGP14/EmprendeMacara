var estado_empresa = 'Habilitada'
var txtBuscador = ''

// Función para establecer una cookie, que será necesario para las solicitudes Ajax con Django
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Evento submit que se ejecuta cuando el usuario da click en Guardar perfil
$(document).ready(function () {
    $("#formPerfil").submit(function (e) {
        e.preventDefault();
        var parametros = new FormData($(this)[0]);
        if ($("#txtNewContra").val() != "" | $("#txtConfirContra").val() != "" | $("#txtContraActul").val() != "") {
            if (validarContraseña("#txtNewContra", "#txtConfirContra")) {
                // Se envían los datos del perfil y se guardan
                savePerfil(parametros)
            }
        } else {
            // Se envían los datos del perfil y se guardan
            savePerfil(parametros)
        }
    });
});

// Función que realiza una petición Ajax a una vista Django para guardar los datos del perfil
function savePerfil(parametros) {
    document.querySelector("#btnGuardar").setAttribute("disabled", false);
    document.body.style.cursor = 'wait';
    $.ajax({
        url: '/administradorWeb/save-perfil/',
        type: 'POST',
        data: parametros,
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: false
    }).done(function (data) {
        document.body.style.cursor = 'default';
        document.querySelector("#btnGuardar").removeAttribute("disabled")
        // Si el resultado es 1, la transacción fue realizada correctamente
        if (data.result == "1") {
            if (data.cambioUserContra == "si") {
                $('#cambioUserContra').modal('show');
            } else {
                $('#mensaje_success').modal('show');
            }
        } else if (data.result == "0") {
            Swal.fire({
                icon: 'error',
                text: 'Error al guardar los datos del perfil, por favor intente nuevamente'
            })
        } else {
            Swal.fire({
                icon: 'error',
                text: data.result
            })
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        document.body.style.cursor = 'default';
        document.querySelector("#btnGuardar").removeAttribute("disabled")
        Swal.fire({
            icon: 'error',
            text: 'Error al guardar los datos del perfil, por favor intente nuevamente'
        })
    }).always(function (data) {});
}

// Evento submit de un formulario que realiza una petición Ajax a una vista Django para buscar empresas
$(document).ready(function () {
    $("#formEmpresas").submit(function (e) {
        e.preventDefault();
        var parametros = new FormData($(this)[0]);
        document.querySelector("#btnBuscar").setAttribute("disabled", false);
        document.body.style.cursor = 'wait';
        $.ajax({
            url: '/administradorWeb/buscar-empresa/',
            type: 'POST',
            data: parametros,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false
        }).done(function (data) {
            document.body.style.cursor = 'default';
            document.querySelector("#btnBuscar").removeAttribute("disabled")
            $('#mensaje').empty()
            // Si el resultado diferente de 0, significa se encontraron resultados en la búsqueda
            if (data.jsonEmpresas != "0") {
                if (data.jsonEmpresas.empresa.length > 0) {
                    // Se actualiza la lista de empresas en la interfaz de usuario
                    setEmpresas(data);
                } else {
                    mensaje = '<div class="alert alert-danger mt-3 alert-dismissable">' +
                        '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                        '<strong>¡Ups!</strong>  Parece que no se ha encontrado la empresa.' +
                        '</div>';
                    $("#mensaje").prepend(mensaje)
                }
            } else {
                mensaje = '<div class="alert alert-danger mt-3 alert-dismissable">' +
                    '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                    '<strong>¡Ups!</strong>  Existió un error el buscar la empresa, por favor intente nuevamente.' +
                    '</div>';
                $("#mensaje").prepend(mensaje)
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            document.body.style.cursor = 'default';
            document.querySelector("#btnBuscar").removeAttribute("disabled")
            mensaje = '<div class="alert alert-danger mt-3 alert-dismissable">' +
                '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                '<strong>¡Ups!</strong> Existió un error el buscar la empresa, por favor intente nuevamente.' +
                '</div>';
            $("#mensaje").prepend(mensaje)
        }).always(function (data) {});
    });
});

// Función que filtra las empresas en función de un estado seleccionado
function filterEmpresas() {
    estado_empresa = $("#cmbEstados option:selected").val();
    $('#mensaje').empty()
    getEmpresas();
}

function getEmpresas() {
    // Obtiene una cookie csrftoken
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/administradorWeb/get-empresas/',
        type: 'POST',
        data: {
            "estado": estado_empresa,
            csrfmiddlewaretoken: csrftoken
        },
        dataType: 'json'
    }).done(function (data) {
        // Si el resultado diferente de 0, significa que se cargaron correctamente los datos
        if (data.jsonEmpresas != "0") {
            // Se actualiza la lista de empresas en la interfaz de usuario
            setEmpresas(data);
        } else {
            Swal.fire({
                icon: 'error',
                text: 'Existió un problema al cargar las empresas, por favor actualice nuevamente la página'
            })
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        Swal.fire({
            icon: 'error',
            text: 'Existió un problema al cargar las empresas, por favor actualice nuevamente la página'
        })
    }).always(function (data) {});
}

// Función que actualiza la lista de empresas que se muestran al usuario
function setEmpresas(data) {
    $('#empresas').empty()
    for (var i = 0; i < data.jsonEmpresas.empresa.length; i++) {
        var classIco = ''
        var accion = ''
        if (data.jsonEmpresas.empresa[i].estado == "Habilitada") {
            classIco = 'fas fa-check-circle';
            accion = '<a href="javascript:confirmarAcc(' + data.jsonEmpresas.empresa[i].id_empresa + ',' + "'" + (data.jsonEmpresas.empresa[i].empresa).replace("'", ' ') + "'" + ');" class="btn-deshabilitar">Deshabilitar</a>';
        } else {
            classIco = 'fa fa-ban';
            accion = '<a href="javascript:confirmarAcc(' + data.jsonEmpresas.empresa[i].id_empresa + ',' + "'" + (data.jsonEmpresas.empresa[i].empresa).replace("'", ' ') + "'" + ');" class="btn-habilitar">Habilitar</a>';
        }
        card = '<div class="notificacion">' +
            '<section class="head">' +
            '<section class="titulo">' +
            '<i class="' + classIco + '"></i>' +
            '<h6 class="m-0">' + data.jsonEmpresas.empresa[i].empresa + '</h6>' +
            '</section >' +
            accion +
            '</section >' +
            '<section class="body">' +
            '<table class="w-100 table-responsive table-condensed">' +
            '<tbody>' +
            '<tr>' +
            '<td class="text-right t-column-width"><strong>Gerente:</strong></td>' +
            '<td class="pl-2">' + data.jsonEmpresas.empresa[i].gerente + '</td>' +
            '</tr>' +
            '<tr>' +
            '<td class="text-right t-column-width"><strong>RUC:</strong></td>' +
            '<td class="pl-2">' + data.jsonEmpresas.empresa[i].ruc + '</td>' +
            '</tr>' +
            '<tr>' +
            '<td class="text-right t-column-widtht"><strong>Actividad comercial:</strong></td>' +
            '<td class="pl-2">' + data.jsonEmpresas.empresa[i].activ_comercial + '</td>' +
            '</tr>' +
            '<tr>' +
            '<td class="text-right t-column-width"><strong>Dirección:</strong></td>' +
            '<td class="pl-2">' + data.jsonEmpresas.empresa[i].direccion + '</td>' +
            '</tr>' +
            '<tr>' +
            '<td class="text-right t-column-width"><strong>Horario de atención:</strong></td>' +
            '<td class="pl-2">' + data.jsonEmpresas.empresa[i].atencion + '</td>' +
            '</tr>' +
            '<tr>' +
            '<td class="text-right t-column-width"><strong>Celular:</strong></td>' +
            '<td class="pl-2">' + data.jsonEmpresas.empresa[i].telefonos + '</td>' +
            '</tr>' +
            '<tr>' +
            '<td class="text-right t-column-width"><strong>Correo:</strong></td>' +
            '<td class="pl-2">' + data.jsonEmpresas.empresa[i].correo + '</td>' +
            '</tr>' +
            '<tr>' +
            '<td class="text-right t-column-width"><strong>Slogan:</strong></td>' +
            '<td class="pl-2">' + data.jsonEmpresas.empresa[i].slogan + '</td>' +
            '</tr>' +
            '<tr>' +
            '<td class="d-flex justify-content-end"><strong>Políticas:</strong></td>' +
            '<td class="pl-1">' + data.jsonEmpresas.empresa[i].politicas + '</td>' +
            '</tr>' +
            '</tbody>' +
            '</table>' +
            '</section>' +
            '</div>';
        $("#empresas").prepend(card);
    }
}

// Función que muestra un mensaje de confirmación para hacer una acción requerida: Habilitar o dehsabilitar una empresa
function confirmarAcc(id_empresa, empresa) {
    if ($("#cmbEstados option:selected").val() == 'Habilitada') {
        swal({
            text: "¿Desea deshabilitar la empresa " + empresa + "?",
            icon: "info",
            buttons: ['NO', 'SI'],
            dangerMode: true
        }).then((value) => {
            // Si es true, significa que respondió SI
            if (value == true) {
                // Se cambia el estado de la empresa
                cambiarEstado(id_empresa, 'Deshabilitada');
            }
        });
    } else {
        swal({
            text: "¿Desea habilitar la empresa " + empresa + "?",
            icon: "info",
            buttons: ['NO', 'SI'],
            dangerMode: true
        }).then((value) => {
            // Si es true, significa que respondió SI
            if (value == true) {
                // Se cambia el estado de la empresa
                cambiarEstado(id_empresa, 'Habilitada');
            }
        });
    }
}

// Función que cambia el estado de una empresa
function cambiarEstado(id_empresa, estado_empresa) {
    // Obtiene una cookie csrftoken
    var csrftoken = getCookie('csrftoken');
    document.body.style.cursor = 'wait';
    $.ajax({
        url: '/administradorWeb/cambiar-estado/',
        type: 'POST',
        data: {
            "id_empresa": id_empresa,
            "estado_empresa": estado_empresa,
            csrfmiddlewaretoken: csrftoken
        },
        dataType: 'json'
    }).done(function (data) {
        // Si el resultado es 1, la transacción fue realizada correctamente
        if (data.result == '1') {
            document.body.style.cursor = 'default';
            // Se filtran las empresas de acuerdo al estado de empresa seleccionado 
            filterEmpresas();
            if (estado_empresa == 'Habilitada') {
                Swal.fire({
                    icon: 'success',
                    text: 'Empresa deshabilitada exitosamente'
                })
            } else {
                Swal.fire({
                    icon: 'success',
                    text: 'Empresa habilitada exitosamente'
                })
            }
        } else {
            document.body.style.cursor = 'default';
            if (estado_empresa == 'Habilitada') {
                Swal.fire({
                    icon: 'error',
                    text: 'Error al deshabilitar la empresa, por favor intente nuevamente'
                })
            } else {
                Swal.fire({
                    icon: 'error',
                    text: 'Error al habilitar la empresa, por favor intente nuevamente'
                })
            }
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        document.body.style.cursor = 'default';
        Swal.fire({
            icon: 'error',
            text: 'Error al cambiar el estado de la empresa, por favor intente nuevamente'
        })
    }).always(function (data) {});
}

// Evento submit del formulario que realiza una petición Ajax a una vista Django para buscar solicitudes
$(document).ready(function () {
    $("#formSolicitud").submit(function (e) {
        e.preventDefault();
        var parametros = new FormData($(this)[0]);
        document.querySelector("#btnBuscar").setAttribute("disabled", false);
        document.body.style.cursor = 'wait';
        $.ajax({
            url: '/administradorWeb/buscar-solicitud/',
            type: 'POST',
            data: parametros,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false
        }).done(function (data) {
            document.body.style.cursor = 'default';
            document.querySelector("#btnBuscar").removeAttribute("disabled")
            $('#mensaje').empty()
            // Si el resultado diferente de 0, significa se encontraron resultados en la búsqueda
            if (data.jsonEmpresas != "0") {
                if (data.jsonEmpresas.empresa.length > 0) {
                    // Se actualiza la lista de solicitudes en la interfaz de usuario
                    setSolicitudes(data);
                } else {
                    mensaje = '<div class="alert alert-danger mt-3 alert-dismissable">' +
                        '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                        '<strong>¡Ups!</strong>  Parece que no se ha encontrado la solicitud.' +
                        '</div>';
                    $("#mensaje").prepend(mensaje)
                }
            } else {
                mensaje = '<div class="alert alert-danger mt-3 alert-dismissable">' +
                    '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                    '<strong>¡Ups!</strong>  Existió un error el buscar la solicitud, por favor intente nuevamente.' +
                    '</div>';
                $("#mensaje").prepend(mensaje)
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            document.body.style.cursor = 'default';
            document.querySelector("#btnBuscar").removeAttribute("disabled")
            mensaje = '<div class="alert alert-danger mt-3 alert-dismissable">' +
                '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                '<strong>¡Ups!</strong>  Existió un error el buscar la solicitud, por favor intente nuevamente.' +
                '</div>';
            $("#mensaje").prepend(mensaje)
        }).always(function (data) {});
    });
});

// Función que realiza una petición Ajax a una vista Django para obtener todas las solicitudes de empresas
function getSolicitudes() {
    // Obtiene una cookie csrftoken
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/administradorWeb/get-solicitudes/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: csrftoken
        },
        dataType: 'json'
    }).done(function (data) {
        // Si el resultado diferente de 0, significa que se cargaron correctamente los datos
        if (data.jsonEmpresas != "0") {
            // Se actualiza la lista de solicitudes en la interfaz de usuario
            setSolicitudes(data);
        } else {
            Swal.fire({
                icon: 'error',
                text: 'Existió un problema al cargar las solicitudes, por favor actualice nuevamente la página'
            })
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        Swal.fire({
            icon: 'error',
            text: 'Existió un problema al cargar las solicitudes, por favor actualice nuevamente la página'
        })
    }).always(function (data) {});
}

// Función que actualiza la lista de solicitudes que se muestran al usuario
function setSolicitudes(data) {
    $('#solicitudes').empty()
    $('#mensaje').empty()
    for (var i = 0; i < data.jsonEmpresas.empresa.length; i++) {
        card = '<div class="notificacion">' +
            '<section class="head">' +
            '<section class="titulo">' +
            '<i class="fas fa-check-circle"></i>' +
            '<h6 class="m-0">' + data.jsonEmpresas.empresa[i].empresa + '</h6>' +
            '</section>' +
            '</section>' +
            '<section class="body">' +
            '<table class="w-100 table-responsive table-condensed">' +
            '<tbody>' +
            '<tr>' +
            '<td class="text-right t-column-width"><strong>Gerente:</strong></td>' +
            '<td class="pl-2">' + data.jsonEmpresas.empresa[i].gerente + '</td>' +
            '</tr>' +
            '<tr>' +
            '<td class="text-right t-column-width"><strong>RUC:</strong></td>' +
            '<td class="pl-2">' + data.jsonEmpresas.empresa[i].ruc + '</td>' +
            '</tr>' +
            '<tr>' +
            '<td class="text-right t-column-widtht"><strong>Actividad comercial:</strong></td>' +
            '<td class="pl-2">' + data.jsonEmpresas.empresa[i].activ_comercial + '</td>' +
            '</tr>' +
            '<tr>' +
            '<td class="text-right t-column-width"><strong>Dirección:</strong></td>' +
            '<td class="pl-2">' + data.jsonEmpresas.empresa[i].direccion + '</td>' +
            '</tr>' +
            '<tr>' +
            '<td class="text-right t-column-width"><strong>Horario de atención:</strong></td>' +
            '<td class="pl-2">' + data.jsonEmpresas.empresa[i].atencion + '</td>' +
            '</tr>' +
            '<tr>' +
            '<td class="text-right t-column-width"><strong>Celular:</strong></td>' +
            '<td class="pl-2">' + data.jsonEmpresas.empresa[i].telefonos + '</td>' +
            '</tr>' +
            '<tr>' +
            '<td class="text-right t-column-width"><strong>Correo:</strong></td>' +
            '<td class="pl-2">' + data.jsonEmpresas.empresa[i].correo + '</td>' +
            '</tr>' +
            '<tr>' +
            '<td class="text-right t-column-width"><strong>Slogan:</strong></td>' +
            '<td class="pl-2">' + data.jsonEmpresas.empresa[i].slogan + '</td>' +
            '</tr>' +
            '<tr>' +
            '<td class="d-flex justify-content-end"><strong>Políticas:</strong></td>' +
            '<td class="pl-1">' + data.jsonEmpresas.empresa[i].politicas + '</td>' +
            '</tr>' +
            '</tbody>' +
            '</table>' +
            '<section class="acciones">' +
            '<a href="javascript:aceptarSolicit(' + data.jsonEmpresas.empresa[i].id_empresa + ',' + "'" + (data.jsonEmpresas.empresa[i].empresa).replace("'", ' ') + "'" + ');" class="btn-aceptar">Aceptar</a>' +
            '<a href="javascript:confirmRechazar(' + data.jsonEmpresas.empresa[i].id_empresa + ',' + "'" + (data.jsonEmpresas.empresa[i].empresa).replace("'", ' ') + "'" + ');" class="btn-rechazar">Rechazar</a>' +
            '</section>' +
            '</section>' +
            '</div>';
        $("#solicitudes").prepend(card);
    }
}

// Función que muestra un mensaje de confirmación para la aceptación de una solicitud de una empresa
function aceptarSolicit(id_empresa, empresa) {
    swal({
        text: "¿Confirme la aceptación de solicitud de la empresa " + empresa + "?",
        icon: "info",
        buttons: ['NO', 'SI'],
        dangerMode: true
    }).then((value) => {
        // Si es true, significa que respondió SI
        if (value == true) {
            // Obtiene una cookie csrftoken
            var csrftoken = getCookie('csrftoken');
            document.body.style.cursor = 'wait';
            $.ajax({
                url: '/administradorWeb/aceptar-solicitud/',
                type: 'POST',
                data: {
                    "id_empresa": id_empresa,
                    csrfmiddlewaretoken: csrftoken
                },
                dataType: 'json'
            }).done(function (data) {
                document.body.style.cursor = 'default';
                // Si el resultado es 1, la transacción fue realizada correctamente
                if (data.result == "1") {
                    // Se obtienen las solicitudes de empresas
                    getSolicitudes();
                    Swal.fire({
                        icon: 'success',
                        text: 'Solicitud de empresa aceptada exitosamente, se ha enviado un correo electrónico a la empresa comunicando la aceptación de su solicitud'
                    })
                } else {
                    Swal.fire({
                        icon: 'error',
                        text: 'Error al aceptar la solicitud de la empresa, por favor intente nuevamente'
                    })
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
                document.body.style.cursor = 'default';
                Swal.fire({
                    icon: 'error',
                    text: 'Error al aceptar la solicitud de la empresa, por favor intente nuevamente'
                })
            }).always(function (data) {});
        }
    });
}

// Función que muestra una modal para ingresar el motivo del rechazo de la solicitud
function confirmRechazar(id_empresa, empresa) {
    getModal("Rechazar solicitud de la empresa " + empresa,
        '<section class="col-sm-3 text-center">' +
        '<label for="txtMotivo" class="col-form-label">Motivo: </label>' +
        '</section>' +
        '<section class="col-sm-12">' +
        '<textarea class="form-control" id="txtMotivo" name="txtMotivo" style="height: 135px;"' +
        'placeholder="Ingrese el motivo del rechazo de la solicitud" maxlength="600" required></textarea>' +
        '</section>',
        '<button type="button" class="close" data-dismiss="modal" aria-label="Close"> <span aria-hidden="true">&times;</span></button>',
        '<button type="button" class="btn btn-danger" data-dismiss="modal">Cancelar</button>' +
        '<a class="btn btn-success" id="btnRechazar" href="javascript:rechazarSolicit(' + "'" + id_empresa + "'" + ');"><i class="fa fa-paper-plane" aria-hidden="true"></i> Rechazar</a>');
}

// Función para realizar el rechazo la solicitud de una empresa
function rechazarSolicit(id_empresa) {
    motivo = $("#txtMotivo").val()
    // Obtiene una cookie csrftoken
    var csrftoken = getCookie('csrftoken');
    document.body.style.cursor = 'wait';
    $.ajax({
        url: '/administradorWeb/rechazar-solicitud/',
        type: 'POST',
        data: {
            "id_empresa": id_empresa,
            "motivo": motivo,
            csrfmiddlewaretoken: csrftoken
        },
        dataType: 'json'
    }).done(function (data) {
        document.body.style.cursor = 'default';
        // Si el resultado es 1, la transacción fue realizada correctamente
        if (data.result == "1") {
            $('#ventana_modal').modal('hide');
            // Se obtienen las solicitudes de empresas
            getSolicitudes();
            Swal.fire({
                icon: 'success',
                text: 'Solicitud de empresa rechazada exitosamente, se ha enviado el correo electrónico a la empresa comunicando el rechazo de la solicitud'
            })
        } else {
            Swal.fire({
                icon: 'error',
                text: 'Error al rechazar la solicitud de la empresa, por favor intente nuevamente'
            })
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        document.body.style.cursor = 'default';
        Swal.fire({
            icon: 'error',
            text: 'Error al rechazar la solicitud de la empresa, por favor intente nuevamente'
        })
    }).always(function (data) {});
}