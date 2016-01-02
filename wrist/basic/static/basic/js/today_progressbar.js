// JavaScript Document
function setStep(){
	$('.circle').each(function(index, el) {
        var num = $(this).find('#per_plan').text() * 3.6;
		var bnum = $(this).find('#persleep_plan').text() * 3.6;
        if (num<=180) {
			if (bnum <= 180){
            	$(this).find('.right').css('transform', "rotate(" + num + "deg)");
			}
			else {
				$(this).find('.left').css('transform', "rotate(0deg)");
				setTimeout('$(".circle").find(".right").css("transform", "rotate(" + ' + num + ' + "deg)")', 500);
			}
        } else {
			if (bnum <= 180){
				$(this).find('.right').css('transform', "rotate(180deg)");
				setTimeout('$(".circle").find(".left").css("transform", "rotate(" + (' + num + '- 180) + "deg)")', 500);
			}
            else {
				$(this).find('.left').css('transform', "rotate(" + (num - 180) + "deg)");
			}
		}
    });
}

function setSleep(){
	$('.circle').each(function(index, el) {																																																				
        var num = $(this).find('#persleep_plan').text() * 3.6;
		var bnum = $(this).find('#per_plan').text() * 3.6;
        if (num<=180) {
			if (bnum <= 180){
            	$(this).find('.right').css('transform', "rotate(" + num + "deg)");
			}
			else {
				$(this).find('.left').css('transform', "rotate(0deg)");
				setTimeout('$(".circle").find(".right").css("transform", "rotate(" + ' + num + ' + "deg)")', 500);
			}
        } else {
			if (bnum <= 180){
				$(this).find('.right').css('transform', "rotate(180deg)");
				setTimeout('$(".circle").find(".left").css("transform", "rotate(" + (' + num + '- 180) + "deg)")', 500);
			}
            else {
				$(this).find('.left').css('transform', "rotate(" + (num - 180) + "deg)");
			}
		}
    });
}
$(function() {
    $('.circle').each(function(index, el) {
	    var num = $(this).find('#per_plan').text() * 3.6;
		var bnum = $(this).find('#persleep_plan').text() * 3.6;
        if (num<=180) {
            $(this).find('.right').css('transform', "rotate(" + num + "deg)");
        } else {
            $(this).find('.right').css('transform', "rotate(180deg)");
			setTimeout('$(".circle").find(".left").css("transform", "rotate(" + (' + num + '- 180) + "deg)")', 500);
        };
    });
	$('#step').click(function(){
		setStep();
		$('#sleep').css("color", "green");
		$('#step').css("color", "orange");
		$('.top').css("background", "#039CFD");
		$('.mask').css("background", "#039CFD");
		$('.circle').css("background", "#FF9328");
		$('.sleepmask').css("display", "none");
		$('.mask').css("display", "inline");
	});
	$('#sleep').click(function(){
		setSleep();
		$('#sleep').css("color", "orange");
		$('#step').css("color", "green");
		$('.top').css("background", "#3F00B4");
		$('.sleepmask').css("background", "#3F00B4");
		$('.circle').css("background", "#9100FF");
		$('.sleepmask').css("display", "inline");
		$('.mask').css("display", "none");
	});
});