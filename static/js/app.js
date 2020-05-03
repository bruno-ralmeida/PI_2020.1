/*  COMPONENTES CUSTOM  */

/*  LOGIN  */
$(".i-login input").on("focus",
  function(){
    $(this).addClass("focus");}
  );
  
$(".i-login input").on("blur",
  function(){
  if($(this).val() == "")
    $(this).removeClass("focus");}
  );


  $('#btn-ipdf').on('click', function () {
    $('.arquivo').trigger('click');
  });

  $('.arquivo').on('change', function () {
    var fileName = $(this)[0].files[0].name;
    $('#file').val(fileName);
  });

