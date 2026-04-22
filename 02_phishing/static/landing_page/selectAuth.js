$(function () {
    $(".idp-button-idp-logo").click(function () {
        $("#indexIdp").val($(".idp-button-idp-logo").index($(this)));
        $("#SPIDform").submit();
    });

															
    $("#cookie-open").click(function (e) {
        $(".bar").slideToggle();
        $(".bs-info-modal-lg2").modal('show');
        e.preventDefault();
    });

    $("#cookie-close").click(function (e) {
        $(".bar").slideToggle();
        e.preventDefault();
    });
	
	$(".spid-gateway-button").click(function(e){
		e.preventDefault();
		var form = $(this).parents('form:first');
		form.submit();
	});
	
	
	$(".cc-btn").click(function(){
		$(".cc-window").hide();
	});

});

$(window).on('load', function () {
    if ($("#SPIDform").length > 0) {
        var left = $("#SPIDform").outerWidth() - $(".italia-it-button").outerWidth();
        if (left > 0)
            left = left / 2;
        $('.spid-idp-button-menu').css({left: left});
    }
});

$(window).resize(function () {
    if ($("#SPIDform").length > 0) {
        var left = $("#SPIDform").outerWidth() - $(".italia-it-button").outerWidth();
        if (left > 0)
            left = left / 2;
        $('.spid-idp-button-menu').css({left: left});
    }
});

$(function () {
    
	
	 /* if($(".wrapper-tondi").size()>4) {
		  var tondiPlus = $(".wrapper-tondi").size() % 4;
		  console.log(tondiPlus);
		 console.log($(".wrapper-tondi").slice(-tondiPlus));
		 ($(".wrapper-tondi").slice(-tondiPlus)).wrap("<div class='wrap-banner-info mx-auto col-md-11 font-weight-bold' id='innerWrapTondi'></div>");
		 $("#innerWrapTondi").css("display", "flex");
		 $("#innerWrapTondi").css("padding-top", "15px");
	  } else if ($(".wrapper-tondi").size() == 8) {
		 ($(".wrapper-tondi").slice(-4)).wrap("<div class='wrap-banner-info mx-auto col-md-11 font-weight-bold' id='innerWrapTondi'></div>");
		 $("#innerWrapTondi").css("padding-top", "15px");
	} */
	  
	  if($(".wrapper-tondi").length<4){
		  $(".wrap-banner-info").css("display","flex");
	}
	  
	if($(".wrapper-tondi").length>4) {
		 var indexWrapper = Math.ceil(($(".wrapper-tondi").length - 4) / 4);
		  var tondiPlus = $(".wrapper-tondi").length % 4;
		  console.log(tondiPlus);
		 console.log($(".wrapper-tondi").slice(-tondiPlus));
	
		console.log("Numeri di wrapper" + indexWrapper);
	
		for (let i = 0; i < indexWrapper; i++) {
			if ((indexWrapper - i == 1) && (tondiPlus != 0)) {
				let array = $(".wrapper-tondi").slice(-tondiPlus);
				console.log(array);
				array.wrapAll("<div class='wrap-banner-info mx-0 font-weight-bold' id='innerWrapTondi" + i + "'></div>");
			
				$("#innerWrapTondi" + i).css("display", "flex");
				$("#innerWrapTondi" + i).css("float", "left");
				$("#innerWrapTondi" + i).css("padding-top", "1%");
				$("#innerWrapTondi" + i).css("width", "100%");
				console.log("Ultimo con eccesso");
		
			} else {
				let start = (i * 4) + 4;
				
				$(".wrap-banner-info").css("display","flex");
				$(".wrap-banner-info").css("flex-wrap","wrap");
				
				console.log("In mezzo");
			} 
			
		}
		
	  }  


	$("body").on("click", ".box-fornitore",function () {
		$("#indexIdp").val($(".box-fornitore").index($(this)));
		$("#SPIDform").submit();
	});
	
	$("#formBasicUnicoAria").on("submit", function() {
		$("input[name='loginUnicoAria']").val("true");
	})
	
	$("form").on("submit",function(){
	setTimeout(function(){
	if($(".std-input-error").length>0){
	
		$("html, body").animate({ 
		specialEasing: {
      height: "easeOutCirc"
    },
		
		scrollTop: $('.std-input-error').first().offset().top - $(".wrapper-fixed-header").height() - "60" }, 1000);
		$(".std-input-error").first().focus();
		
	}}, 500);
	
	
	
	});
	
	
	$(window).scroll(function() { 
  
  $('nav').removeClass("d-flex");
  if ($(document).scrollTop() > 75) {
    $('nav').slideUp(); 
  } else {
    $('nav').slideDown();
  }
});


});




$(function () {
	if(!(window.attachEvent && !window.addEventListener)) {
	window.cookieconsent.initialise({
	  "palette": {
		"popup": {
		  "background": "#0066cc",
		  "text": "#ffffff"
		},
		"button": {
		  "background": "#0066cc",
		  "text": "#ffffff"
		}
	  },
	  "content": {
		"message": "<span class='cookie_info_1'><strong>Questo sito utilizza <em>cookie</em> tecnici. Proseguendo nella navigazione accetti l'utilizzo dei cookie.</strong> <br/></span> <span class='cookie-info-2'>Per maggiori informazioni, <a data-toggle='modal' data-target='#modal-id-cookie'><u> leggi l'informativa completa.</u></a></span>",
		"dismiss": "<span style='text-decoration: none;'>X</span>",
		"link": ""
	  },
	  "cookie": {
		  "domain": "crs.lombardia.it"
	  }
	});
	}
});