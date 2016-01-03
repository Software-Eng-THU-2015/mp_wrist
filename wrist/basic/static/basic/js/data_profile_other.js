var userId = $("#userId").attr("userId");

$(".plan").click(function(){
   window.location.href = $(".link").attr("to").replace("basic", "plan") + "?page=4&id=" + $(this).attr("userId"); 
});

$(".match").click(function(){
   window.location.href = $(".link").attr("to").replace("basic", "match") + "?page=3&id=" + $(this).attr("userId");
});

$(".friend").click(function(){
    var node = $(this);
    var flag = 0;
    node.toggleClass("btn-danger");
    node.toggleClass("btn-success");
    if(node.hasClass("btn-danger")){
        node.html("删除好友");
        flag = 1;
    }
    else{
        node.html("加为好友");
        flag = 0;
    }
    var url = domain + "/basic/add/friend?userId=" + userId + "&target=" + node.attr("userId") + "&type=" + str(flag);
    getData(url, function(){});
});