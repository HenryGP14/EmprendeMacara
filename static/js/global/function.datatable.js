$(document).ready(function () {
    var table = $("#detalles_compra").DataTable({
        order: [],
        language: {
            select: {
                rows: {
                    _: "%d registros seleccionados",
                    0: "No se han seleccionado registros",
                    1: "1 registro seleccionado",
                },
            },
            emptyTable: "No hay datos disponibles en la tabla.",
            info: "Mostrando la página _PAGE_ de _PAGES_",
            infoEmpty: "Mostrando 0 registros de un total de 0.",
            infoFiltered: "(filtrados _TOTAL_ registros)",
            lengthMenu: "Mostrar _MENU_ registros",
            loadingRecords: "Cargando...",
            processing: "Procesando...",
            search: "Buscar:",
            searchPlaceholder: "Dato para buscar",
            zeroRecords: "No se han encontrado coincidencias.",
            paginate: {
                first: "Primera",
                last: "Última",
                next: "Siguiente",
                previous: "Anterior",
            },
            aria: {
                sortAscending: "Ordenación ascendente",
                sortDescending: "Ordenación descendente",
            },
        },
        lengthMenu: [
            [5, 10, 20, 25, 50, -1],
            [5, 10, 20, 25, 50, "Todos"],
        ],
        iDisplayLength: 10,
    });
});