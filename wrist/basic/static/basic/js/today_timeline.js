// JavaScript Document
$(function() {
    var ulNode = $('ul.timeline');
	var liNodes = ulNode.find('li'), count = liNodes.length, i, liNode;
	for (i=0; i< count; i++){
		liNode = $(liNodes.get(i));
		if (i % 2 !== 0){
			liNode.addClass('alt');
		}
		else {
			liNode.removeClass('alt');
		}
	}
});