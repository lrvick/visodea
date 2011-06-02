$(document).ready(function() {

$("input:checkbox").css('width', '16px');

//////////////////////////////
// LOG IN PANEL //////////////
// Expand Panel
$("#open").click(function(){
	$("div#panel").slideDown(400);
});	
// Collapse Panel
$("#close").click(function(){
	$("div#panel").slideUp(400);	
});		
// Switch buttons from "Log In | Register" to "Close Panel" on click
$("#toggle a").click(function () {
	$("#toggle a").toggle();
});		


// Pretty up search box
$("input[name='q']").focus(function(){
	if($(this).val()=="search opportunities") {
		$(this).val("");
	}
});

$("input[name='q']").blur(function(){
	if($(this).val()=="") {
		$(this).val("search opportunities");
	}
});

$("input[type='text']").focus(function(){
	var itsName = $(this).attr("title");
	if($(this).val()==itsName) {
		$(this).val("");
	}
});

$("input[type='text']").blur(function(){
	var itsName = $(this).attr("title");
	if($(this).val()=="") {
		$(this).val(itsName);
	}
});
// Select Boxes
$(".rCol select").sSelect({
	ddMaxHeight: '300px'
});

// Project "Share" dropdowns //////////
var config = {    
     sensitivity: 2, // number = sensitivity threshold (must be 1 or higher)    
     interval: 50,  // number = milliseconds for onMouseOver polling interval    
     over: doOpen,   // function = onMouseOver callback (REQUIRED)    
     timeout: 50,   // number = milliseconds delay before onMouseOut    
     out: doClose    // function = onMouseOut callback (REQUIRED)    
};

function doOpen() {
    $(this).addClass("hover");
    $('ul:first',this).css('visibility', 'visible');
}

function doClose() {
    $(this).removeClass("hover");
    $('ul:first',this).css('visibility', 'hidden');
}

$("ul.dropdown li").hoverIntent(config);	


$(".shareLinks li").click(function(){

	var title = $(this).parent().attr("id"); 
	var id = $(this).attr("id"),
    	currentUrl = window.location.href,
		baseUrl = $(this).find("a").attr("title");

	if (id.indexOf("twitter") != -1) {
      window.location.href = baseUrl + "/home?status=http://visodea.com/project/" + title.toLowerCase();
    } else if (id.indexOf("facebook") != -1) {
      window.location.href = baseUrl + "/sharer.php?u=http://visodea.com/project/" + title.toLowerCase() + "&t=" + title;
    }
	
});
//////////////////////////

// Project progress bars - jQuery UI component
$("#progressbar").each(function(){
	var percent = $(this).attr('title');
	$(this).progressbar({
			value: percent
	});
});
//////////////////////////
$("#mt").accordion({
	collapsible: true
});

//end DomReady	
});