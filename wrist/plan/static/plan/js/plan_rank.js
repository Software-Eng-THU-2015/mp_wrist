var userId = $("#userId").attr("userId");

$('.follow.button').click(function(){
   var node = $(this);
   node.toggleClass('blue');
   var URL = domain + "/plan/data/follow?&user=" + userId + "&target=" + $(this).attr("userId");
   getData(URL, function(){});
   if(node.hasClass("blue"))
       node.html('<i class="paw icon"></i>Following');
   else
       node.html('<i class="paw icon"></i>&nbsp&nbsp&nbsp&nbspFollow&nbsp&nbsp&nbsp');
});

$(".profileLink").click(function(){
    window.location.href = $(".link").attr("to") + "?page=4&id=" + $(this).attr("userId");
});