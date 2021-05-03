/**
 * handle counter
 */
;
(function () {
    'use strict';
    $.fn.handleCounter = function (options) {
        var $input,
            $btnMinus,
            $btnPlugs,
            num_minimo,
            num_maximo,
            se_escribe,
            onChange,
            onMinimum,
            onMaximize;
        var $handleCounter = this
        $btnMinus = $handleCounter.find('.btn-decrementar')
        $input = $handleCounter.find('input')
        $btnPlugs = $handleCounter.find('.btn-incrementar')
        var defaultOpts = {
            se_escribe: true,
            num_minimo: 1,
            num_maximo: null,
            onChange: function () {},
            onMinimum: function () {},
            onMaximize: function () {}
        }
        var settings = $.extend({}, defaultOpts, options)
        num_minimo = settings.num_minimo
        num_maximo = settings.num_maximo
        se_escribe = settings.se_escribe
        onChange = settings.onChange
        onMinimum = settings.onMinimum
        onMaximize = settings.onMaximize

        if (!$.isNumeric(num_minimo)) {
            num_minimo = defaultOpts.num_minimo
        }
        if (!$.isNumeric(num_maximo)) {
            num_maximo = defaultOpts.num_maximo
        }

        var inputVal = $input.val()
        if (isNaN(parseInt(inputVal))) {
            inputVal = $input.val(0).val()
        }
        if (!se_escribe) {
            $input.prop('disabled', true)
        }

        changeVal(inputVal)
        $input.val(inputVal)
        $btnMinus.click(function () {
            var num = parseInt($input.val())
            if (num > num_minimo) {
                $input.val(num - 1)
                changeVal(num - 1)
            }
        })
        $btnPlugs.click(function () {
            var num = parseInt($input.val())
            if (num_maximo == null || num < num_maximo) {
                $input.val(num + 1)
                changeVal(num + 1)
            }
        })

        var keyUpTime
        $input.keyup(function () {
            clearTimeout(keyUpTime)
            keyUpTime = setTimeout(function () {
                var num = $input.val()
                if (num == '') {
                    num = num_minimo
                    $input.val(num_minimo)
                }
                var reg = new RegExp("^[\\d]*$")
                if (isNaN(parseInt(num)) || !reg.test(num)) {
                    $input.val($input.data('num'))
                    changeVal($input.data('num'))
                } else if (num < num_minimo) {
                    $input.val(num_minimo)
                    changeVal(num_minimo)
                } else if (num_maximo != null && num > num_maximo) {
                    $input.val(num_maximo)
                    changeVal(num_maximo)
                } else {
                    changeVal(num)
                }
            }, 300)
        })
        $input.focus(function () {
            var num = $input.val()
            if (num == 0) $input.select()
        })

        function changeVal(num) {
            $input.data('num', num)
            $btnMinus.prop('disabled', false)
            $btnPlugs.prop('disabled', false)
            if (num <= num_minimo) {
                $btnMinus.prop('disabled', true)
                onMinimum.call(this, num)
            } else if (num_maximo != null && num >= num_maximo) {
                $btnPlugs.prop('disabled', true)
                onMaximize.call(this, num)
            }
            onChange.call(this, num)
        }
        return $handleCounter
    };
})(jQuery)