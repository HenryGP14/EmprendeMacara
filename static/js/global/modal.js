function getModal(md_titulo, md_mensaje, md_opcHeader, md_opcFooter) {
    $('#ventana_modal').modal({backdrop: 'static', keyboard: false})
    document.querySelector("#md_titulo").innerHTML = "<strong>" + md_titulo + "</strong>";
    document.querySelector("#md_mensaje").innerHTML = md_mensaje;
    document.querySelector("#md_opcHeader").innerHTML = md_opcHeader;
    document.querySelector("#md_opcFooter").innerHTML = md_opcFooter;
    $('#ventana_modal').modal('show');
}

$("#ventana_modal").on('hidden.bs.modal', function () {
    document.querySelector("#md_titulo").innerHTML = "";
    document.querySelector("#md_mensaje").innerHTML = "";
    document.querySelector("#md_opcHeader").innerHTML = "";
    document.querySelector("#md_opcFooter").innerHTML = "";
});