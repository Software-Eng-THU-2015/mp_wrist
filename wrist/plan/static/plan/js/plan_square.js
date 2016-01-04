$('.follow.button').
	state({
	    text:{
		inactive : '<i class="paw icon"></i>Follow',
		active: '<i class="paw icon"></i>Following'
	    }
	});
    
var userId = $("#userId").attr("userId");

$('.follow.button').click(function(){
   $(this).toggleClass('blue');
   var URL = domain + "/plan/data/follow?&user=" + userId + "&target=" + $(this).attr("userId");
   getData(URL, function(){});
});


$('.like.button').click(function(){
   $(this).toggleClass('red');
   var URL = domain + "/basic/data/goods?type=1&user=" + userId + "&target=" + $(this).attr("userId");
   getData(URL, function(){});
});

$(".profileLink").click(function(){
   window.location.href = $(".link").attr("to") + "?page=4&id=" + $(this).attr("userId"); 
});