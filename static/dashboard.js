
$(document).ready(function() {
	$('#fullpage').fullpage({
		//Navigation
		// menu: '#menu',
		// lockAnchors: false,
		// anchors:['firstPage', 'secondPage'],
		navigation: false,
		navigationPosition: 'right',
		// navigationTooltips: ['firstSlide', 'secondSlide'],
		showActiveTooltip: false,
		slidesNavigation: false,
		slidesNavPosition: 'bottom',

		//Scrolling
		css3: true,
		scrollingSpeed: 700,
		autoScrolling: true,
		fitToSection: true,
		fitToSectionDelay: 1000,
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
		sectionsColor : ['#ccc', '#fff'],
		paddingTop: '0',
		paddingBottom: '0px',
		fixedElements: '#header, .footer',
		responsiveWidth: 0,
		responsiveHeight: 0,
		responsiveSlides: false,
		parallax: false,
		parallaxOptions: {type: 'reveal', percentage: 62, property: 'translate'},

		//Custom selectors
		sectionSelector: '.section',
		slideSelector: '.slide',

		lazyLoading: true,

		//events
		onLeave: function(index, nextIndex, direction){},
		afterLoad: function(anchorLink, index){},
		afterRender: function(){},
		afterResize: function(){},
		afterResponsive: function(isResponsive){},
		afterSlideLoad: function(anchorLink, index, slideAnchor, slideIndex){},
		onSlideLeave: function(anchorLink, index, slideIndex, direction, nextSlideIndex){}
	});

 $('#fadeandscale').popup();
$('#fadeandscale').popup('show');
	// check_net_amt();

	preloaderFadeOutTime = 500;
function hidePreloader() {
var preloader = $('.spinner-wrapper');
preloader.fadeOut(preloaderFadeOutTime);
}
setTimeout(
  function() 
  {
    hidePreloader();
  }, 2500);

});

var amt = $('#net').text();
var x = parseInt(amt);
	if (x < 0) {
		$('#net').css("color",'red');
	}
	else{
		$('#net').css("color",'green');
	}

$('#fadeandscale').popup({
  transition: 'all 0.3s'
});


$('#bid').on('change',function () {
	var bid = $('#bid').val();
	// alert(bid);
	var url = "/show_bills/" + bid;
	// alert(url);
	window.location.href = "show_bills/" + bid;
});

$(document).on('keyup keypress', function(e) {
  var keyCode = e.keyCode || e.which;
  if (keyCode === 13) { 
    e.preventDefault();
    return false;
}
});