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
      var tpl = $($(".template")[1]).html();
      var template = Handlebars.compile(tpl);
      $(".tip.modal").html(template());
      $("#matchModal").modal("show");
  }
});
