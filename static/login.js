$('.toggle').on('click', function() {
  $('.container').stop().addClass('active');
});

$('.close').on('click', function() {
  $('.container').stop().removeClass('active');
});
$('.reg2').on('click', function() {
	$('.container').stop().addClass('active');
});
$('.log2').on('click', function(){
	$('.container').stop().removeClass('active');
});