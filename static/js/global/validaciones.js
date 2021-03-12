
function soloLetras(event) {
    var regex = new RegExp("^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
        event.preventDefault();
        return false;
    }
}

function soloNumeros(event) {
    var regex = new RegExp("^[0-9]+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
        event.preventDefault();
        return false;
    }
}

function soloLetrasNumeros(event) {
    var regex = new RegExp("^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9 ]+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
        event.preventDefault();
        return false;
    }
}

function soloDirecciones(event) {
    var regex = new RegExp("^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9 ].,\-+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
        event.preventDefault();
        return false;
    }
}
function soloDolares(event) {
    var regex = new RegExp("^(?(?!0)(d{1,3},?){1,3}|0)(.[0-9]{1,2})?$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
        event.preventDefault();
        return false;
    }
}

function validarContraseña(password, repassword) {
    //Se remueven los mensajes de validacion existentes
    $('.validate-smock').remove();
    //Se inicializan las variables
    var result = false;
    //Se crea la expresion regular para la contraseña
		var strongPassRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])\w{6,}$/; // Debe contener al menos 6 caracteres, un numero y una mayuscula
		//Se obtiene el title de password
		var txtrequiredPass = $(password).attr('title');
		//Si password no contiene title se asigna un mensaje de validacion default
		if (txtrequiredPass === '' || txtrequiredPass === undefined) {
			txtrequiredPass = 'La contraseña debe tener al menos 6 caracteres, un número, una mayúscula y minúscula';
		}
    //Se obtiene el title de repassword
    var txtrequiredRePass = $(repassword).attr('title');
    //Si repassword no contiene title se asigna un mensaje de validacion default
    if (txtrequiredRePass === '' || txtrequiredRePass === undefined) {
        txtrequiredRePass = 'Las contraseñas no coinciden';
    }
    //Si password esta vacio o no cumple con la expresion regular requerida se retorna false
		if ($(password).val() === '' || !strongPassRegex.test($(password).val())) {
			$(password).focus().after('<span class="validate-smock text-danger">' + txtrequiredPass + '</span>');
			result = false;
			return false;
		} else { //Si no esta vacio y cumple con la expresion regular requerida se retorna true
			result = true;
		}
        if ($(repassword).val() === '' || !strongPassRegex.test($(repassword).val())) {
			$(repassword).focus().after('<span class="validate-smock text-danger">' + txtrequiredPass + '</span>');
			result = false;
			return false;
		} else { //Si no esta vacio y cumple con la expresion regular requerida se retorna true
			result = true;
		}
    //Si se teclea algo en password se remueven los mensajes de validacion
    $(password).keyup(function () {
        if ($(this).val() !== '') {
            $('.validate-smock').fadeOut('fast');
            return false;
        }
    });
    $(repassword).keyup(function () {
        if ($(this).val() !== '') {
            $('.validate-smock').fadeOut('fast');
            return false;
        }
    });

    //Si los password son diferentes se retorna false
    if ($(password).val() !== $(repassword).val()) {
        $(repassword).focus().after('<span class="validate-smock text-danger">' + txtrequiredRePass + '</span>');
        result = false;
        return false;
    } else { //Si los passwords son iguales se retorna true
        result = true;
    }
    //Se retorna el resultado
    return result;
}

