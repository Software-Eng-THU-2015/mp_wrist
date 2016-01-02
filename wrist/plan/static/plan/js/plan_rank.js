$('.follow.button').
	state({
	    text:{
		inactive : '<i class="paw icon"></i>&nbsp&nbsp&nbsp&nbspFollow&nbsp&nbsp&nbsp',
		active: '<i class="paw icon"></i>Following'
	    }
	});
    
var userId = $("#userId").attr("userId");

$('.follow.button').click(function(){
   $(this).toggleClass('blue');
   var URL = domain + "/plan/data/follow?&user=" + userId + "&target=" + $(this).attr("userId");
   getData(URL, function(){});
});

