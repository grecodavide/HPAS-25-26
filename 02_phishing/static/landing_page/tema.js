$(".backButton").parent().click(function(){
	var form = $(this).parents('form:first');
	form.prop("action", "SSLAuthServlet");
	form.unbind('submit').submit();
});

$(".backButtonWrapper").parent().click(function(){
	$("#back").submit();
}); 

 $(".psw-show-hide").click(function(){

if($("#password").attr("type")=="text"){
	$("#password").attr("type","password");
	$(this).attr("src","/staticResources/images/new/occhio-chiuso@2x.png");
	}
else{
	$("#password").attr("type","text");
	$(this).attr("src","/staticResources/images/new/occhio-aperto@2x.png");}

});

 $(".psw-show-hide-ap-1").click(function(){
	if($("#newPassId").attr("type")=="text"){ 
$("#newPassId").attr("type","password");
$(this).attr("src","/staticResources/images/new/occhio-chiuso@2x.png");
	}
else{
	$("#newPassId").attr("type","text");
	$(this).attr("src","/staticResources/images/new/occhio-aperto@2x.png");}

});


 $(".psw-show-hide-ap-2").click(function(){
	if($("#renewPassId").attr("type")=="text"){ 
$("#renewPassId").attr("type","password");
$(this).attr("src","/staticResources/images/new/occhio-chiuso@2x.png");
	}
else{
	$("#renewPassId").attr("type","text");
	$(this).attr("src","/staticResources/images/new/occhio-aperto@2x.png");}

});



 $("#occhio-half-1").click(function(){
	 if($("#input-accedi-password-half-1").attr("type")=="text"){
	$("#input-accedi-password-half-1").attr("type","password");
	 $(this).attr("src","/staticResources/images/new/occhio-chiuso@2x.png");}
	 else{
		 $("#input-accedi-password-half-1").attr("type","text");
	 $(this).attr("src","/staticResources/images/new/occhio-aperto@2x.png");
		 
	 }
});


 $("#occhio-half-2").click(function(){
	 if($("#input-accedi-password-half-2").attr("type")=="text"){
	$("#input-accedi-password-half-2").attr("type","password");
	 $(this).attr("src","/staticResources/images/new/occhio-chiuso@2x.png");}
	 else{
		 $("#input-accedi-password-half-2").attr("type","text");
	 $(this).attr("src","/staticResources/images/new/occhio-aperto@2x.png");
		 
	 }
});

$(function(){
	if($("form").length > 0 && typeof token !== "undefined"){
	    $("form").not("#back").append("<input type='hidden' name='token' value='"+token+"'/>");
	}else if($("form").length > 0 && typeof tokenNewTab !== "undefined"){
		$("form").not("#back").append("<input type='hidden' name='tokenNewTab' value='"+tokenNewTab+"'/>");
	}
});

/* Login */
 
  $("#login").submit(function(e){
	$("#errore-utente-mancante").hide();
	  $("#errore-password-mancante").hide();
    var nomeUtente = $("#input-accedi-id").val();
    var psw = $("#input-accedi-password").val();
    if(nomeUtente == "" && psw == ""){
	  //alert("Inserire nome utente e password");
	  $("#errore-utente-mancante").show();
	  
      e.preventDefault();
    }else if(nomeUtente == ""){
	$("#errore-utente-mancante").show();
	  
      e.preventDefault();
    }else if(psw == ""){
	  //alert("Inserire la password");
	  $("#errore-password-mancante").show();
      
      e.preventDefault();
    }else{
      //$(":submit").prop('disabled', true);
    }
  });

/* End Login */

/* funzione accessibilità mostra nascondi password */

function access_psw(event){
		  if (event.keyCode === 13) {
			event.target.children[0].click();
		  }
}
