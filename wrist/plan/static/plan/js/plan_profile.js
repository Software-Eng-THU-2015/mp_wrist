var userId = $("#userId").attr("userId");

$('.follow.button').click(function(){
   var URL = domain + "/plan/follow?&user=" + userId + "&target=" + $(this).attr("userId");
   getData(URL, function(){});
});


$('.like.button').click(function(){
   $(this).toggleClass('red');
   var URL = domain + "/basic/goods?type=1&user=" + userId + "&target=" + $(this).attr("userId");
   getData(URL, function(){});
});