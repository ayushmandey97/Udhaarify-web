$('#amount').on('change',function () {
		$(this).css('background-color','#9effb5');
})
$(document).on('keyup keypress', function(e) {
  var keyCode = e.keyCode || e.which;
  if (keyCode === 13) { 
    e.preventDefault();
    return false;
}
});