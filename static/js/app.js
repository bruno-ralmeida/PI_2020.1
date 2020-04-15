/*COMPONENTES CUSTOM*/
$(".i-login input").on("focus",
  function(){
    $(this).addClass("focus");}
  );
  
$(".i-login input").on("blur",
  function(){
  if($(this).val() == "")
    $(this).removeClass("focus");}
  );

