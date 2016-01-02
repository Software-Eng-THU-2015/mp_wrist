// JavaScript Document
$(function(){
	var fst = $('.list-group-item').get(1);
	$(fst).next().css('display','block');
	$(fst).addClass('list-group-item-success');
	$('.list-group-item').click(function(e){
		$('.group-info').css('display','none');
		$('.list-group-item').removeClass('list-group-item-success');
		$(e.target).addClass('list-group-item-success');
		var tar = $(e.target).next();
		$(tar).css('display','block');
	});
});