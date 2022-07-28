$(function() { 
	var u, n, t, r, i; 
	jssor_1_slider_init = function(n, t) { 
		var jssor_1_slider = new $JssorSlider$(n, t) 
		var MAX_WIDTH = 3000;

        function ScaleSlider() {
            var containerElement = jssor_1_slider.$Elmt.parentNode;
            var containerWidth = containerElement.clientWidth;
            
            if (containerWidth) {

                var expectedWidth = Math.min(MAX_WIDTH || containerWidth, containerWidth);

                jssor_1_slider.$ScaleWidth(expectedWidth);
            }
            else {
                window.setTimeout(ScaleSlider, 30);
            }
        }

        ScaleSlider();
                                        
        //Scale slider while window load/resize/orientationchange.
        $Jssor$.$AddEvent(window, "load", ScaleSlider);
        $Jssor$.$AddEvent(window, "resize", ScaleSlider);
        $Jssor$.$AddEvent(window, "orientationchange", ScaleSlider);
	}, 
    $("#slider1_container").length > 0 && (
    	u = [{ $Duration: 1200, y: .3, $During: { $Top: [.3, .7] }, $Easing: { $Top: $Jease$.$InCubic, $Opacity: $Jease$.$Linear }, $Opacity: 2, $Outside: !0 }], 
    	$('*[data-u="caption"]').length && $('*[data-u="caption"]').each(function(n) { $(this).attr("data-t", n) }), 
    	n = [], 
    	t = $("#slider1_container").data("event-theme"),
    	n.push([{ b: -1, d: 1, o: -1 }, { b: 1800, d: 600, x: -55, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 1800, d: 600, x: 30, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 900, d: 900, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 0, d: 500, x: 45, y: 38, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 380, d: 600, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 800, d: 600, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 2100, d: 500, y: -52, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 2300, d: 400, x: 96, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 1800, d: 500, y: -127, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 1500, d: 800, y: 5, o: 1, e: { o: 14 } }], [{ b: -1, d: 1, o: -1, sX: -.5 }, { b: 2100, d: 500, o: 1, sX: .5 }], [{ b: -1, d: 1, o: -1, sX: -.5 }, { b: 2100, d: 500, o: 1, sX: .5 }], [{ b: -1, d: 1, o: -1 }, { b: 1700, d: 600, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 1700, d: 600, o: 1 }]), 
    	n.push([{ b: -1, d: 1, o: -1, sX: -.9, sY: -.9 }, { b: 0, d: 1700, x: 820, y: 144, o: 1, sX: .9, sY: .9 }], [{ b: 0, d: 1700, x: -1105, y: 12 }], [{ b: -1, d: 1, o: -1, sX: -.5, sY: -.5 }, { b: 2e3, d: 100, o: .8 }, { b: 2100, d: 1800, o: .2, r: 360 }, { b: 3900, d: 400, o: -.3 }, { b: 4300, d: 400, o: .3 }, { b: 4700, d: 400, o: -.2 }, { b: 5100, d: 300, o: .2 }], [{ b: -1, d: 1, o: -1 }, { b: 2e3, d: 1e3, y: 4, o: 1 }], [{ b: -1, d: 1, r: -45 }, { b: 2200, d: 600, x: -42, y: 462, e: { y: 30 } }, { b: 2800, d: 200, x: 9, y: 2, r: 45, e: { r: 29 } }], [{ b: -1, d: 1, r: 45 }, { b: 2400, d: 600, x: -24, y: 455, e: { y: 30 } }, { b: 3e3, d: 200, x: 11, y: 11, r: -45, e: { r: 30 } }], [{ b: -1, d: 1, r: -45 }, { b: 2600, d: 600, x: -85, y: 533, e: { y: 30 } }, { b: 3200, d: 200, x: 4, y: 7, r: 60 }], [{ b: -1, d: 1, o: -1 }, { b: 2100, d: 100, o: .8 }, { b: 2200, d: 1800, o: .2, r: 360 }, { b: 4e3, d: 400, o: -.3 }, { b: 4400, d: 400, o: .3 }, { b: 4800, d: 400, o: -.2 }, { b: 5200, d: 400, o: .2 }], [{ b: -1, d: 1, o: -1 }, { b: 1900, d: 100, o: .8 }, { b: 2e3, d: 1800, o: .2, r: 360 }, { b: 3800, d: 400, o: -.3 }, { b: 4200, d: 400, o: .3 }, { b: 4600, d: 400, o: -.2 }, { b: 5e3, d: 400, o: .2 }], [{ b: -1, d: 1, o: -1, sX: -.3, sY: -.3 }, { b: 1600, d: 100, o: .8 }, { b: 1700, d: 1800, o: .2, r: 360 }, { b: 3500, d: 400, o: -.3 }, { b: 3900, d: 400, o: .3 }, { b: 4300, d: 400, o: -.2 }], [{ b: -1, d: 1, c: { t: -304 } }, { b: 1600, d: 800, y: 1, c: { t: 304 } }]), 
    	n.push([{ b: -1, d: 1, o: -1 }, { b: 2e3, d: 1e3, x: -280, y: 77, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 1e3, d: 1e3, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 2100, d: 900, x: 237, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 1200, d: 800, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 0, d: 1e3, o: 1, e: { o: 14 } }], [{ b: -1, d: 1, o: -1 }, { b: 1300, d: 700, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 2500, d: 700, y: -199, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 2800, d: 800, y: -207, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 2800, d: 800, y: 264, o: 1 }]), 
    	n.push([{ b: -1, d: 1, o: -1 }, { b: 2e3, d: 900, x: -243, o: 1, e: { x: 1, o: 1 } }], [{ b: -1, d: 1, o: -1 }, { b: 1e3, d: 600, x: -130, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 2e3, d: 440, rX: 180, rY: 180 }, { b: 2440, d: 460, o: 1, rX: 180, rY: 180 }], [{ b: -1, d: 1, o: -1 }, { b: 1300, d: 700, x: 173, o: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 0, d: 1e3, o: 1 }], [{ b: -1, d: 1, o: -1, sX: -1, sY: -1 }, { b: 2900, d: 1100, o: 1, sX: 1, sY: 1 }], [{ b: -1, d: 1, o: -1, sX: -1, sY: -1 }, { b: 3100, d: 900, o: 1, sX: 1, sY: 1 }], [{ b: -1, d: 1, o: -1 }, { b: 1400, d: 600, o: 1 }]), 
    	r = n, 
    	i = { $AutoPlay: !0, $SlideDuration: 800, $DragOrientation: 0, $SlideshowOptions: { $Class: $JssorSlideshowRunner$, $Transitions: u }, $CaptionSliderOptions: { $Class: $JssorCaptionSlideo$, $Transitions: r }, $ArrowNavigatorOptions: { $Class: $JssorArrowNavigator$ }, $BulletNavigatorOptions: { $Class: $JssorBulletNavigator$ } }, 
    	jssor_1_slider_init("slider1_container", i)
    ),
	$("#jssor_game_banner").length > 0 && (
		r = [
            [{ b: -1, d: 1, o: -1 }, { b: 0, d: 1e3, o: 1 }],
            [{ b: -1, d: 1, o: -1 }, { b: 0, d: 1e3, o: 1 }],
            [{ b: -1, d: 1, o: -1 }, { b: 0, d: 1e3, o: 1 }],
            [{ b: -1, d: 1, o: -1 }, { b: 0, d: 1e3, o: 1 }],
            [{ b: -1, d: 1, o: -1 }, { b: 1e3, d: 1e3, o: 1 }],
            [{ b: -1, d: 1, o: -1 }, { b: 0, d: 1e3, o: 1 }],
            [{ b: -1, d: 1, o: -1 }, { b: 0, d: 1e3, o: 1 }],
            [{ b: -1, d: 1, o: -1 }, { b: 0, d: 1e3, o: 1 }],
            [{ b: -1, d: 1, o: -1 }, { b: 0, d: 1e3, o: 1 }],
            [{ b: -1, d: 1, o: -1 }, { b: 0, d: 1e3, o: 1 }],
            [{ b: -1, d: 1, c: { t: -281 } }, { b: 1e3, d: 1e3, y: 1, c: { t: 281 } }],
            [{ b: -1, d: 1, o: -1 }, { b: 1800, d: 1200, o: 1 }],
            [{ b: -1, d: 1, o: -1 }, { b: 1800, d: 1200, o: 1 }]
        ], 
        i = { $AutoPlay: !0, $SlideDuration: 800, $SlideEasing: $Jease$.$OutQuint, $CaptionSliderOptions: { $Class: $JssorCaptionSlideo$, $Transitions: r }, $ArrowNavigatorOptions: { $Class: $JssorArrowNavigator$ }, $BulletNavigatorOptions: { $Class: $JssorBulletNavigator$ } }, 
        jssor_1_slider_init("jssor_game_banner", i)
    )
});

$(document).ready(function ($) {
	var jackpot_increase_timer;
	var pub = $('body').data('publisher');
	var curCode = $('body').data('currency-code');

    $(".jackpot-light-circle").animateSprite({ 
		fps: 3, 
		animations: { 
			walkLeft: [0, 1, 2] 
		}, 
		loop: !0, 
		duration: 300
	});

    $(".jackpot-coin").animateSprite({ 
		fps: 12, 
		animations: { 
			walkLeft: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
		}, 
		loop: !0, 
		duration: 500
	});

    // Back to top
    var backToTop = $("#back-to-top");
	if(backToTop.length) {
	    var sticky = 400;
	    $(window).scroll(function() {
	        if ($(window).scrollTop() >= 400) {
	            backToTop.removeClass("fadeout");
	          } else {
	            backToTop.addClass("fadeout");
	          }
	    });

	    backToTop.find('a').click(function(e) {
	    	e.preventDefault();
            $('html, body').animate({
                scrollTop: 0
            }, 1000);
        });
	}

	// Contact button
	$('.contact-collapse').on('click', function(e){
        e.preventDefault();
		$(this).next().toggleClass('collapse-width');
	});
});

function numberWithCommas(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}