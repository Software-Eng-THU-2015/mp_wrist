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
   var URL = "http://wrist.ssast2015.com/plan/follow?&user=" + userId + "&target=" + $(this).attr("userId");
   getData(URL, function(){});
});


$('.like.button').click(function(){
   $(this).toggleClass('red');
   var URL = "http://wrist.ssast2015.com/basic/goods?type=1&user=" + userId + "&target=" + $(this).attr("userId");
   getData(URL, function(){});
});