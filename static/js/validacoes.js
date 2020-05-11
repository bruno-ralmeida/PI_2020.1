$(document).ready(function () {
    var url_medico = $('#url_medico').val();
    var url_paciente = $('#url_paciente').val();

    $('#id_cpf').mask('999.999.999-99');
    $('#id_rg').mask('99.9969.999-9');
    $('#id_data_nasc').mask('99/99/9999');
    $('#id_tel').mask('(11) 9999-9999');
    $('#id_cel').mask('(11) 99999-99999');

    $('#id_cpf').on('input', function () {
      var form = new FormData($('#form')[0]);
      $.ajax({
        type: "POST",
        cache: false,
        processData: false,
        contentType: false,
        url: url_paciente,
        data: form,
        success: function (data) {
          $("#id_paciente").html('<option value="" selected="selected">Selecione</option>')
          data.forEach(paciente => {
            let id = paciente["id"]
            let nome = paciente['nome']
            $("#id_paciente").append('<option value="' + id + '">' + nome + '</option>');
          });
        },
      });
    });


    $('.dt_hr').on('input', function () {
      now = new Date();
      let hora_atual = now.getHours() + ':' + now.getMinutes();
      let data_atual = now.getDate();
      let data_aux = $('#id_data').val();
      let hora_form = $('#id_hora').val();
      let aux = data_aux.split('/');
      let data_form = Number(aux[0]);

      if (data_form == data_atual) {
        if (hora_form < hora_atual) {
          $('#id_hora').val(now.getHours() + ':00');
        }
      }
      var form = new FormData($('#form')[0]);
      $.ajax({
        type: "POST",
        cache: false,
        processData: false,
        contentType: false,
        url: url_medico,
        data: form,
        success: function (data) {
          $("#id_medico").html('<option value="" selected="selected">Selecione</option>')
          data.forEach(medico => {
            let id = medico["id"]
            let nome = medico['nome']
            $("#id_medico").append('<option value="' + id + '">' + nome + '</option>');
          });
        },
      });
    });
  });