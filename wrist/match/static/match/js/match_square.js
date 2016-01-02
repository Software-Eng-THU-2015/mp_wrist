$('.follow.button').
	state({
	    text:{
		inactive : '<i class="paw icon"></i>&nbsp&nbsp&nbsp&nbspJoin&nbsp&nbsp&nbsp',
		active: '<i class="paw icon"></i>Joined'
	    }
	});
    
var userId = $("#userId").attr("userId");

$('.follow.button').click(function(){
  var URL = domain + "/match/join?user=" + userId + "&target=" + $(this).attr("userId");
  if($(this).hasClass('blue'))
      getData(URL, function(){});
  else{
      var modal = $("#matchModal");
      if(modal.hasClass("in")){
          modal.css({"display":
          "none"});
      }
      else{
          modal.css({"display": "block","padding-left":"0px"});
      }
      modal.toggleClass("in");
  }
});
