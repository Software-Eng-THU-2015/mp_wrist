$('.follow.button').
	state({
	    text:{
		inactive : '<i class="paw icon"></i>&nbsp&nbsp&nbsp&nbspFollow&nbsp&nbsp&nbsp',
		active: '<i class="paw icon"></i>Following'
	    }
	});

$('.follow.button').click(function(){
   $(this).toggleClass('blue');
   var URL = "http://wrist.ssast2015.com/plan/follow?&user=" + userId + "&target=" + $(this).attr("userId");
   getData(URL, function(){});
});

