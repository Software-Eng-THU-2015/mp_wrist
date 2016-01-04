var userId = $("#userId").attr("userId");

$('.follow.button').click(function(){
  var node = $(this);
  var URL = domain + "/plan/data/follow?userId=" + userId + "&target=" + $(this).attr("userId");
  getData(URL, function(){});
  node.toggleClass("btn-success");
  node.toggleClass("btn-danger");
  if(node.hasClass('btn-success'))
      node.html("加入计划");
  else
      node.html("取消计划");
});

$('.like.button').click(function(){
   $(this).toggleClass('red');
   var URL = domain + "/basic/data/goods?type=1&user=" + userId + "&target=" + $(this).attr("userId");
   getData(URL, function(){});
});

var node = $(".ui.progress");

node.progress("reset");

node.progress({
    total: parseInt(node.attr("total")),
    value: parseInt(node.attr("value"))
});