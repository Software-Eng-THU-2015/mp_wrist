$('.follow.button').
	state({
	    text:{
		inactive : '<i class="paw icon"></i>Follow',
		active: '<i class="paw icon"></i>Following'
	    }
	});

$('.follow.button').click(function(){
      $(this).toggleClass('blue');
    });


$('.like.button').click(function(){
      $(this).toggleClass('red');
    });
