
if($("body").hasClass("english_page")){
		document.cookie = "language=en";
}

var linguaCorrente = document.cookie.split(';').filter(function(item) {
  if(item.indexOf('language=')<0){
  return "it";}
  else{
  return item.indexOf('language=') >= 0}
})[0].split('=')[1];

if(linguaCorrente!='en'&&linguaCorrente!='it'){
	linguaCorrente = 'it';
	document.cookie = "language=it";
}


$(document).ready(function(){





var lingua = "";

if(linguaCorrente=="it"){
	
$("#translatePage .italiano,#translatePageMobile .italiano").css("text-decoration","underline");
$("#translatePage .english,#translatePage .english").css("text-decoration","none");	
document.cookie = "language=it";

	
}else{
$("#translatePage .italiano,#translatePageMobile .italiano").css("text-decoration","none");
$("#translatePage .english,#translatePageMobile .english").css("text-decoration","underline");	
document.cookie = "language=en";
	
$("#translatePage .fa").addClass("translating");

	i18next
			.use(i18nextXHRBackend)
			.init(
					{
						"lng" : "en",
						"fallbackLng" : "IT",
						"getAsync" : false,
						"backend" : {
							"loadPath" : function(lngs, namespaces) {
								return "static/landing_page/idpc_lang_"+linguaCorrente+".json";
							},
							"allowMultiLoading" : false,
							"parse" : function(data) {
								return JSON.parse(data);
							},
							"crossDomain" : false,
							"withCredentials" : false
						}
					}, function() {
						
						
$("#translatePage .fa").removeClass("translating");
							jqueryI18next.init(i18next, $);
							try{
								$('body').localize(); // localize del body
								self.openInANewTabTitle();
							} catch(e){
								
							}
							
						
						
					});



}
	
});




$(document).ready(function(){


$("body").on('click', ".italiano", function(){ $(".italiano").css("text-decoration","underline"); $(".english").css("text-decoration","none");
document.cookie = "language=it";
linguaCorrente = "it";
});

$("body").on('click', ".english", function(){ $(".english").css("text-decoration","underline"); $(".italiano").css("text-decoration","none");
document.cookie = "language=en";
linguaCorrente = "en";
});




$("#translatePage,#translatePageMobile a").on('click', function(){
//translatePage("en");



/*
if(linguaCorrente=="it"){
	//$("#translatePage .italiano").show();
//$("#translatePage .english").hide();	
document.cookie = "language=en";
linguaCorrente= "en";
//$("#translatePage .fa").addClass("translating");
	
}else{
//$("#translatePage .italiano").hide();
//$("#translatePage .english").show();	
document.cookie = "language=it";
linguaCorrente= "it";

}
*/


/*
if(linguaCorrente=="it"){
	//linguaCorrente="en";
//$("#translatePage .fa").addClass("translating");
}else{
	//linguaCorrente= "it";
	
//$("#translatePage .fa").addClass("translating");
}
*/

// recupera lingua da un div
				

	/***************************************************************************
	 *  i18next 
	 **************************************************************************/

	// aggiunto getAsync = a false.
	
	i18next
			.use(i18nextXHRBackend)
			.init(
					{
						"lng" : "en",
						"fallbackLng" : "IT",
						"getAsync" : false,
						"backend" : {
							"loadPath" : function(lngs, namespaces) {
								return "static/landing_page/idpc_lang_"+linguaCorrente+".json";
							},
							"allowMultiLoading" : false,
							"parse" : function(data) {
								return JSON.parse(data);
							},
							"crossDomain" : false,
							"withCredentials" : false
						}
					}, function() {
							
							jqueryI18next.init(i18next, $);
							try{
								$('body').localize(); // localize del body
								self.openInANewTabTitle();
							} catch(e){
								
							}
							
//$("#translatePage .fa").removeClass("translating");
						
					});






});




});


