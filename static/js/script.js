function toggleTable(tableId, buttonId) {
    var table = document.getElementById(tableId);
    var button = document.getElementById(buttonId);
    if (table.style.display === "none") {
        table.style.display = "";
        button.innerHTML = "-";
    } else {
        table.style.display = "none";
        button.innerHTML = "+";
    }
};

$(document).ready(function() {
    $('#tabela_transacoes').DataTable({
        "language": {"url": "https://cdn.datatables.net/plug-ins/1.10.22/i18n/Portuguese-Brasil.json"},
        "paging": false,
        "columnDefs": [
            { "type": "date-eu", "targets": 5 },
            { "type": "date-eu", "targets": 6 }
        ],
        "order": [[ 6, 'asc' ]]
    });
});


function populateForm(editButton) {

    let id = editButton.getAttribute('data-transaction-id')
    let descricao = editButton.getAttribute('data-transaction-descricao')
    let conta_id = editButton.getAttribute('data-transaction-conta-id')
    let tipo = editButton.getAttribute('data-transaction-tipo')
    let data_evento = editButton.getAttribute('data-transaction-data-evento')
    let data_execucao = editButton.getAttribute('data-transaction-data-execucao')
    let valor = editButton.getAttribute('data-transaction-valor')



    // Preencher formulário com os valores recuperados
    document.getElementById('editar_transacao_id').value = id;
    document.getElementById('editar_transacao_descricao').value = descricao;
    document.getElementById('editar_transacao_conta').value = conta_id;
    document.getElementById('editar_transacao_tipo').value = tipo;
    document.getElementById('editar_transacao_data_evento').value = data_evento ;
    document.getElementById('editar_transacao_data_execucao').value = data_execucao;
    document.getElementById('editar_transacao_valor').value = valor ;
    document.getElementById('editar_transacao_quantidade_meses').value = 1;


}
