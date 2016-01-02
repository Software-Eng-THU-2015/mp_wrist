$('.follow.button').
	state({
	    text:{
		inactive : '<i class="paw icon"></i>&nbsp&nbsp&nbsp&nbspJoin&nbsp&nbsp&nbsp',
		active: '<i class="paw icon"></i>Joined'
	    }
	});
    
var userId = $("#userId").attr("userId");

$('.follow.button').click(function(){
  var URL = domain + "/data/match/join?user=" + userId + "&target=" + $(this).attr("userId");
  if($(this).hasClass('blue'))
      getData(URL, function(){});
  else
  {
      $(".join-group").empty();
      var tpl = $(".template")[1].html();
      var template = Handlebars.compile(tpl);
      getData(URL, function(data){
          var json = eval("(" + data + ")");
          $(".join-group").html(template(json));
          $(".join-group").css({"display": "inline"});
      });
  }
});

$("#cancel").click(function(){
   $(".join-group").empty(); 
   $(".join-group").css({"display": "none"});
});

$("#join").click(function(){
   var selected = $(".list-group-item-success");
   var URL = domain + "/data/www/match/join?user=" + userId + "&target=" + $(this).attr("userId") + "&team=";
   if(selected.length == 0)
       getData(URL + "-1", function(){});
   else
       getData(URL, function(){});
   $("#cancel").click();
});