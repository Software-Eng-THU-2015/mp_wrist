// JavaScript Document
$(function(){
	var bts = $('.foot').find('button');
    var id = parseInt($(".data").attr("page"));
	$(bts).click(function(e){
		window.location.href = $(".link").attr("to") + "?page=" + $(this).attr("page");
	});
    if(id < bts.length){
	var mpg = bts.get(id);
	$(mpg).css('color','#F7BE2E');
    }
});