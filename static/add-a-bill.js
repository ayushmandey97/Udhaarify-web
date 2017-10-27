//**************************************//

    //SPA TRANSITIONS

//**************************************//

$(document).ready(function() {
    $('#fullpage').fullpage({
        //Navigation
        menu: '#menu',
        lockAnchors: false,
        navigation: false,
        navigationPosition: 'right',
        navigationTooltips: ['firstSlide', 'secondSlide'],
        showActiveTooltip: false,
        slidesNavigation: false,
        slidesNavPosition: 'bottom',

        //Scrolling
        css3: true,
        scrollingSpeed: 500,
        autoScrolling: true,
        fitToSection: true,
        fitToSectionDelay: 200,
        scrollBar: false,
        easing: 'easeInOutCubic',
        easingcss3: 'ease',
        loopBottom: false,
        loopTop: false,
        loopHorizontal: true,
        continuousVertical: false,
        continuousHorizontal: false,
        scrollHorizontally: false,
        interlockedSlides: false,
        dragAndMove: false,
        offsetSections: false,
        resetSliders: false,
        fadingEffect: false,
        normalScrollElements: '#element1, .element2',
        scrollOverflow: false,
        scrollOverflowReset: false,
        scrollOverflowOptions: null,
        touchSensitivity: 15,
        normalScrollElementTouchThreshold: 5,
        bigSectionsDestination: null,

        //Accessibility
        keyboardScrolling: true,
        animateAnchor: true,
        recordHistory: true,

        //Design
        controlArrows: false,
        verticalCentered: true,
        // sectionsColor : ['#ccc', '#fff'],
        paddingTop: '200px',
        paddingBottom: '200px',
        borderRadius: '70px',
        // fixedElements: '#header, .footer',
        // responsiveWidth: 0,
        // responsiveHeight: 0,
        // responsiveSlides: false,
        // parallax: false,
        // parallaxOptions: {type: 'reveal', percentage: 62, property: 'translate'},

        //Custom selectors
        sectionSelector: '.section',
        slideSelector: '.slide',

        lazyLoading: false,

        //events
        onLeave: function(index, nextIndex, direction){},
        afterLoad: function(anchorLink, index){},
        afterRender: function(){},
        afterResize: function(){},
        afterResponsive: function(isResponsive){},
        afterSlideLoad: function(anchorLink, index, slideAnchor, slideIndex){
            // var loadedSlide = $(this);
            if(index == 1 && slideIndex == 3){
                console.log('loaded')
            renderSubmit();
        }
        },
        onSlideLeave: function(anchorLink, index, slideIndex, direction, nextSlideIndex){}
    });
});


    

//**************************************//

    //SPA RENDER AND BUTTON-EVENT-CONTROL

//*************************************//


renderDescriptionPage();
$('#next1').on("click", function () {
    $.fn.fullpage.moveTo(1, 1);
});
$('#next2').on("click", function () {
    $.fn.fullpage.moveTo(1, 2);
});
$('#next3').on("click", function () {
    $.fn.fullpage.moveTo(1, 3);
});
$('#prev1').on("click", function(){
    $.fn.fullpage.moveSlideLeft();
});
$('#prev2').on("click", function(){
    $.fn.fullpage.moveSlideLeft();
});
$('#prev3').on("click", function(){
    $.fn.fullpage.moveSlideLeft();
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



/*$("#addflist").keypress(function(event){
    if (event.which === 13) {
        //grabbing new todo text from input
        var newFriend = $("#addflist").val();
        $(this).val("");
        //create a new li and add to ul
        $("#flist").append("<li class='list-group-item'>"+newFriend+"<span class='glyphicon glyphicon-remove' aria-hidden='true' class='xbutton'> </span></li>" );
    }   
});
*/
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

/*$('#seq').click(function() {
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
});*/


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

$(function() {
    $("div[data-toggle=fieldset]").each(function() {
        var $this = $(this);
        
        //Add new entry
        $this.find("button[data-toggle=fieldset-add-row]").click(function() {
            var target = $($(this).data("target"))
            // console.log(target);
            var oldrow = target.find("[data-toggle=fieldset-entry]:last");
            var row = oldrow.clone(true, true);
            // console.log(row.find(":input")[0]);
            var elem_id = row.find(":input")[0].id;
            var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})-.*/m, '$1')) + 1;
            row.attr('data-id', elem_num);
            row.find(":input").each(function() {
                // console.log(this);
                var id = $(this).attr('id').replace('-' + (elem_num - 1) + '-', '-' + (elem_num) + '-');
                $(this).attr('name', id).attr('id', id).val('').removeAttr("checked");
            });
            oldrow.after(row);
        }); //End add new entry

        //Remove row
        $this.find("button[data-toggle=fieldset-remove-row]").click(function() {
            if($this.find("[data-toggle=fieldset-entry]").length > 1) {
                var thisRow = $(this).closest("[data-toggle=fieldset-entry]");
                thisRow.remove();
            }
        }); //End remove row
        //focus shift
    });
});

$('.addftext').keypress(function (event) {
    if(event.which==13){
        console.log('hello')
        $('#addbtn1').click();
    }
})

$('.PTEXT').keypress(function (event) {
    if(event.which==13){
        // console.log('hello')
        $('#addbtn2').click();
   if ($('#peq').is(':checked')) {
        var n = $('#paidtable tr').length;
        var amt = $('#amount').val()/(n);
        console.log(amt);
        var x = $(".PAMT");
        x.val(amt.toFixed(2));
    }
}
})
$('.PAMT').keypress(function (event) {
    if(event.which==13){
        // console.log('hello')
        $('#addbtn2').click();
    if ($('#peq').is(':checked')) {
        var n = $('#paidtable tr').length;
        var amt = $('#amount').val()/(n-1);
        console.log(amt);
        $(".form-control PAMT").text(amt.toFixed(2));
    }
}
    
})
$('.SBYTEXT').keypress(function (event) {
    if(event.which==13){
        // console.log('hello')
        $('#addbtn3').consolelick();
        if ($('#seq').is(':checked')) {
        var n = $('#splittable tr').length;
        var amt = $('#amount').val()/(n);
        // console.log(amt);
        var x = $(".SAMT");
        x.val(amt.toFixed(2));
    }
    }
})
$('.SAMT').keypress(function (event) {
    if(event.which==13){
        // console.log('hello')
        $('#addbtn3').click();
    }
})

$('#peq').click(function() {
  if ($(this).is(':checked')) {
    $(".PAMT").attr("disabled","disabled");
}
else{
    $(".PAMT").removeAttr("disabled");
    $("#peq").removeAttr('checked');
}
});

$('#seq').click(function() {
  if ($(this).is(':checked')) {
    $(".SAMT").attr("disabled","disabled");
}
else{
    $(".SAMT").removeAttr("disabled");
    $("#seq").removeAttr('checked');
}
});


$('.Prmv').on("click", function(){
    console.log("hello")
    if ($('#peq').is(':checked')) {
        // console.log('hello');
        var n = $('#paidtable tr').length;
        if (n!=1) {
        var amt = $('#amount').val()/(n-1);
        // console.log(amt);
        var x = $(".PAMT");
        x.val(amt.toFixed(2));
        }
    }
})

$('.Srmv').on("click", function(){
    console.log("hello")
    if ($('#seq').is(':checked')) {
        // console.log('hello');
        var n = $('#splittable tr').length;
        if (n!=1) {
        var amt = $('#amount').val()/(n-1);
        // console.log(amt);
        var x = $(".SAMT");
        x.val(amt.toFixed(2));
        }
    }
})
//**************************************//

    //SPA FUNCTION DEFINITIONS

//*************************************//

/*function init() {
  var all = $('.page');
  all.addClass('hide');
  all.removeClass('show');
  var submitbtn = $('.submitbtn');
  submitbtn.removeClass('show');
  submitbtn.addClass('hide');
}*/

function renderDescriptionPage(){


    var render = $('.bdescription');
    render.addClass('show');
}
function renderFriendsPage(){


    var render = $('.addfriends');
    render.addClass('show');
}
function renderPaidByPage(){


    var render = $('.paidby');
    render.addClass('show');
}
function renderSplitAmongst() {


 var render = $('.splitamongst');
 render.addClass('show');
}
function renderSubmit() {
    var render = $('#addbill');
    render.removeClass('hide');
    render.fadeIn();
}
//**************************************//

        //OTHER FUNCTION DEFINITIONS

//*************************************//
/*function pcheck() {
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
};*/