/*------------- ScrollToTop --------------- */
$(window).scroll(function(){
	if ($(this).scrollTop() > 200) {
	$('.scrollToTop').fadeIn();
} else {
	$('.scrollToTop').fadeOut();
}
});
$('.scrollToTop').click(function() {
	$('html, body').animate({
		scrollTop : 0
	}, 800);
	return false;
});
/* ---------- slider  -----------*/
$('.slider-content').slick({
    infinite: true,
    slidesToShow: 6,
    slidesToScroll: 6,
    speed: 300,
    dots:true,
    autoplay: true,
	autoplaySpeed: 4000,
    arrows: false,
    rtl:true,            
});
/* ---------- cssmenu  -----------*/
$('#cssmenu li.active').addClass('open').children('ul').show();
	$('#cssmenu li.has-sub>a').on('click', function(){
		$(this).removeAttr('href');
		var element = $(this).parent('li');
		if (element.hasClass('open')) {
			element.removeClass('open');
			element.find('li').removeClass('open');
			element.find('ul').slideUp(200);
		}
		else {
			element.addClass('open');
			element.children('ul').slideDown(200);
			element.siblings('li').children('ul').slideUp(200);
			element.siblings('li').removeClass('open');
			element.siblings('li').find('li').removeClass('open');
			element.siblings('li').find('ul').slideUp(200);
		}
});
/* ---------- step  -----------*/
$('.step').each(function(index, el) {
  $(el).not('.active').addClass('done');
  $('.done').html('<i class="icon-valid"></i>');
  if($(this).is('.active')) {
    $(this).parent().addClass('pulse')
    return false;
  }
});
$('.datepicker').persianDatepicker({
	format: 'YYYY/MM/DD',
	initialValue: false,
});
$('#start-date').persianDatepicker({
	format: 'YYYY/MM/DD',
	initialValue: null,
	maxDate: new persianDate(),
	altField: '#start-observer'
});
$(".showhide").change(function() {
	$show_id = $(this).data("show-id");
	$(".hidden").hide();
	if ($(this).is(":checked")) {
		$("#"+$show_id).show();
	}
});
$(".showhide").each(function() {
	$show_id = $(this).data("show-id");
	if ($(this).is(":checked")) {
		$("#" + $show_id).show();
	}
});
$('.datepicker').persianDatepicker({
	format: 'YYYY/MM/DD',
	initialValue: false,
});
$('#start-date').persianDatepicker({
	format: 'YYYY/MM/DD',
	initialValue: false,
	maxDate: new persianDate(),
});


/* ------------- Crop Images ----------------- */

	
/*------------- MobileMenu --------------- */
$(".header-right-mob").click(function() {
	$('.mob-swipe-bg').show()
	value1 = $('.mobile-menu-right').css('right') === '-260px' ? 0 : '-260px';
	$('.mobile-menu-right').stop().css({
		right : value1
	});
});
$(".mob-swipe-bg").click(function() {
	$('.mob-swipe-bg').hide()
	$(".mobile-menu-right").css("right", "-260px");
});
$(".header-search-mob").click(function() {
	$(".mobile-search").show("slow");
	$(".mobile-search-input").focus();
});
$(".search-close").click(function() {
	$(".mobile-search").hide("slow");
});
