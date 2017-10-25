//**************************************//

    //SAP RENDER AND BUTTON-EVENT-CONTROL

//*************************************//

init();
renderDescriptionPage();
$('#next1').on("click", function () {
	renderFriendsPage();
});
$('#next2').on("click", function () {
	renderPaidByPage();
});
$('#next3').on("click", function () {
	renderSplitAmongst();
});
$('#prev1').on("click", function(){
	renderDescriptionPage();
});
$('#prev2').on("click", function(){
	renderFriendsPage();
});
$('#prev3').on("click", function(){
	renderPaidByPage();
});

//**************************************//

    //OTHER CLICK AND KEYPRESS EVENTS

//*************************************//

$("ul").on("click", "span", function(event){
	$(this).parent().fadeOut(500,function(){
		$(this).remove();
	});
	event.stopPropagation();
});



$("#addflist").keypress(function(event){
	if (event.which === 13) {
		//grabbing new todo text from input
		var newFriend = $("#addflist").val();
		$(this).val("");
		//create a new li and add to ul
		$("#flist").append("<li class='list-group-item'>"+newFriend+"<span class='glyphicon glyphicon-remove' aria-hidden='true' class='xbutton'> </span></li>" );
	}	
});

$("#amt").keypress(function(event){
    if (event.which === 13) {
        //grabbing new todo text from input
        var newFriend = $("#paidbytext").val();
        var amt = $("#amt").val();
        $("#paidbytext").val("");
        $(this).val("");
        //create a new li and add to ul
        $("#paidlist").append("<li class='list-group-item'>"+newFriend);
        $("#pamtlist").append("<li class='list-group-item amounts'>"+amt+"</li>")
    }   
});

$("#samt").keypress(function(event){
    if (event.which === 13) {
        //grabbing new todo text from input
        var newFriend=$("#splitbytext").val();
        var amt = $("#samt").val();
        $("#splitbytext").val("");
        $(this).val("");
        //create a new li and add to ul
        $("#splitlist").append("<li class='list-group-item'>"+newFriend);
        $("#samtlist").append("<li class='list-group-item'>"+amt+"</li>")
    }   
});

$('#seq').click(function() {
  if ($(this).is(':checked')) {
    $("#samt").attr("disabled","disabled");
}
else{
    $("#samt").removeAttr("disabled")
    $("#seq").removeAttr('checked');
}
});

$('#peq').click(function() {
  if ($(this).is(':checked')) {
    $("#amt").attr("disabled","disabled");
}
else{
    $("#amt").removeAttr("disabled");
    $("#peq").removeAttr('checked');
}
});


$("#paidbytext").keypress(function(event){
    if(pcheck()===true){
        if (event.which === 13) {
        //grabbing new todo text from input
        var newFriend = $("#paidbytext").val();
        var n = $('#paidlist').children().length;
        var amt = $('#amount').val()/(n+1);
        $("#paidbytext").val("");
        //create a new li and add to ul
        $("#paidlist").append("<li class='list-group-item'>"+newFriend);
        $('#pamtlist').empty();
        for (var i=0;i<n+1;i++) {  
         $("#pamtlist").append("<li class='list-group-item amounts'>"+amt.toFixed(2)+"</li>")   
     }
 }   
}
});

$("#splitbytext").keypress(function(event){
    if(scheck()===true){
        if (event.which === 13) {
        //grabbing new todo text from input
        var newFriend = $("#splitbytext").val();
        var n = $('#splitlist').children().length;
        var amt = $('#amount').val()/(n+1);
        $("#splitbytext").val("");
        //create a new li and add to ul
        $("#splitlist").append("<li class='list-group-item'>"+newFriend);
        $('#samtlist').empty();
        for (var i=0;i<n+1;i++) {  
         $("#samtlist").append("<li class='list-group-item amounts'>"+amt.toFixed(2)+"</li>")   
     }
 }   
}
});

$("#reset1").click(function () {
    $(".bdescription input").val("");
    $("#notes").val("");
});

$("#reset2").click(function () {
     $("#flist").empty();
});

$('#complete-add-bill').on('keyup keypress', function(e) {
  var keyCode = e.keyCode || e.which;
  if (keyCode === 13) { 
    e.preventDefault();
    return false;
  }
});

//**************************************//

    //SAP FUNCTION DEFINITIONS

//*************************************//

function init() {
  var all = $('.page');
  all.addClass('hide');
  all.removeClass('show');
}

function renderDescriptionPage(){
    init();

    var render = $('.bdescription');
    render.addClass('show');
}
function renderFriendsPage(){
    init();

    var render = $('.addfriends');
    render.addClass('show');
}
function renderPaidByPage(){
    init();

    var render = $('.paidby');
    render.addClass('show');
}
function renderSplitAmongst() {
   init();

   var render = $('.splitamongst');
   render.addClass('show');
}

//**************************************//

        //OTHER FUNCTION DEFINITIONS

//*************************************//
function pcheck() {
  if ($('#peq').is(':checked')) {
    $("#amt").attr("disabled","disabled");
    return true;
}
else{
    $("#amt").removeAttr("disabled");
    $("#peq").removeAttr('checked');
    return false;
}
};
function scheck() {
 if ($('#seq').is(':checked')) {
    $("#samt").attr("disabled","disabled");
    return true;
}
else{
    $("#samt").removeAttr("disabled");
    $("#seq").removeAttr('checked');
    return false;
}
};