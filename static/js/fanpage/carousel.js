$(".owl-carousel").owlCarousel({
	autoplay: true,
	autoplayHoverPause: true,
	autoplayTimeout: 2000,
	items: 2,
	nav: true,
	loop: true,
	responsive: {
		200: {
			items: 1,
			dots: true,
		},
		600: {
			items: 2,
			dots: true,
		},
		1200: {
			items: 3,
			dots: true,
		},
	},
});
