var userId = $("#userId").attr("userId");

$('.follow.button').click(function(){
   var node = $(this);
   node.toggleClass('blue');
   if(node.hasClass("blue"))
       node.html('<i class="paw icon"></i>Following');
   else
       node.html('<i class="paw icon"></i>Follow');
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