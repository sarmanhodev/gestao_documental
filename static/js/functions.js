function get_data_atual() {
    let data_atual = new Date();
    $("#data_atual").html(`<input type="text" id="calendario" name="data_atual" value='${data_atual.toLocaleDateString()}' readonly
                                    class="form-control text-uppercase">
                                    <label for="calendario">Data</label>`)
    console.log(data_atual.toLocaleDateString());
}


function novoCadastro() {
    $("#modalAdicionaCadastro").find("#dossie").val(" ");
    $("#modalAdicionaCadastro").find('#processo').val('');
    $("#modalAdicionaCadastro").find("#parte_contraria").val('');
    $("#modalAdicionaCadastro").find("#comarca").val('');
    $("#modalAdicionaCadastro").find("#cartorio").val('');
    $("#modalAdicionaCadastro").find("#observacoes").val('');
    $("#modalAdicionaCadastro").find("input[name = radio_cliente_novo]:checked").val('');
    $("#modalAdicionaCadastro").find(".nome_cliente").val('');
    $("#modalAdicionaCadastro").find(".select_especialidade").val('');
    $("#modalAdicionaCadastro").find(".select_seguro").val('Selecione uma seguradora');
    $("#modalAdicionaCadastro").find(".valor_recebido").val('');
    $("#modalAdicionaCadastro").find(".valor_receber").val('');

}

function limpar_campos(id) {
    $(`#modalCadastraReu${id}`).find("#tags").val(" ");
    $(`#modalCadastraReu${id}`).find('#tag').val('');
    $(`#modalCadastraReu${id}`).find("#select_seguro").val('');
    $(`#modalCadastraReu${id}`).find("#valor_recebido").val('');
    $(`#modalCadastraReu${id}`).find("#valor_receber").val('');
}


function meses_anos() {
    const month = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
    var d = new Date();
    let mes = month[d.getMonth()];
    let ano = d.getFullYear();
    $("#modalAdicionaCadastro").find("#mes").html(`<input type='text' name='mes_value' value='${mes}'>`)
    $("#modalAdicionaCadastro").find("#ano").html(`<input type='text' name='ano_value' value='${ano}'>`)
}


function meses_anos_reus(id) {
    const month = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
    var d = new Date();
    let mes = month[d.getMonth()];
    let ano = d.getFullYear();
    $(`#modalCadastraReu${id}`).find("#mes_reu").html(`<input type='text' name='mes' value='${mes}'>`);
    $(`#modalCadastraReu${id}`).find("#ano_reu").html(`<input type='text' name='ano' value='${ano}'>`);
}





function pega_nome(id) {
    const nomes = $(`#modalCadastraReu${id}`).find(".nome_cliente").val();
    console.log(nomes);
    event.preventDefault();
    $.ajax({
        url: "/busca_cliente_antigo/" + nomes,
        type: "GET",
        dataType: "json",
        success: function (data) {
            console.log(data[0]);
            if (nomes === '') {
                $(`#modalCadastraReu${id}`).find(".select_especialidade").val('');

            } else {
                console.log(data[0]);
                $(`#modalCadastraReu${id}`).find(".select_especialidade").val(data[0]['especialidade']);
                $(`#modalCadastraReu${id}`).find(".radio_cliente_antigo").html(`<input class="form-check-input slide-toggle status_cliente${id}"
                                            name="radio_cliente_novo" onclick = 'liberar_btn_cadastra_reu(${id})' value="Não" type="radio" checked>
                                        <label class="form-check-label" for="radioClienteAntigo">
                                            Não
                                        </label>`);
            }
            console.log(data);
        },
        error: function () {
            $(`#modalCadastraReu${id}`).find(".select_especialidade").val(``);
            console.log("Registro inexistente");
        },
    });
}

function pegar_nome_cliente() {
    const nomes = $(`#modalAdicionaCadastro`).find(".nome_cliente").val();
    console.log(nomes);
    event.preventDefault();
    $.ajax({
        url: "/busca_cliente_antigo/" + nomes,
        type: "GET",
        dataType: "json",
        success: function (data) {
            console.log(data[0]);
            if (nomes === '') {
                $(`#modalAdicionaCadastro`).find(".select_especialidade").val('');

            } else {
                console.log(data[0]);
                $(`#modalAdicionaCadastro`).find(".select_especialidade").val(data[0]['especialidade']);

                $(`#modalAdicionaCadastro`).find('.status_cliente').find(".radio_cliente_antigo").html(`<input class="form-check-input slide-toggle status_cliente"
                                            name="radio_cliente_novo" onclick = 'liberar_btn_cadastra_reu(this)' value="Não" type="radio" checked>
                                        <label class="form-check-label" for="radioClienteAntigo">
                                            Não
                                        </label>`);
            }
            console.log(data);
        },
        error: function () {
            $(`#modalAdicionaCadastro`).find(".select_especialidade").val(``);
            console.log("Registro inexistente");
        },
    });
}

function liberar_btn_cadastra() {
    const dossie = $('#modalAdicionaCadastro').find('#dossie').val();
    const processo = $('#modalAdicionaCadastro').find('#processo').val();
    const parte_contraria = $('#modalAdicionaCadastro').find('#parte_contraria').val();

    if (dossie === '' || processo.length < 5) {
        $('#modalAdicionaCadastro').find('#btn_cadastra').css({ 'display': 'none' });
    } else {
        $('#modalAdicionaCadastro').find('#btn_cadastra').css({ 'display': 'block' });
    }
}

function liberar_btn_cadastra_reu(id) {
    if ($(`#modalCadastraReu${id}`).find(`.status_cliente${id}`).find('input[name = radio_cliente_novo]:checked').val() || $(`#modalCadastraReu${id}`).find(`.select_seguro${id}`).val() !='') {
        $(`#modalCadastraReu${id}`).find('.btn_save_registro').css({ 'display': 'block' });
    } else {
        $(`#modalCadastraReu${id}`).find('.btn_save_registro').css({ 'display': 'none' });
    }
}
