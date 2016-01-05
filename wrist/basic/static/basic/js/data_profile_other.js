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
    if(node.hasClass("btn-danger")) flag = 1;
    var url = domain + "/basic/add/friend?userId=" + userId + "&target=" + node.attr("userId") + "&type=" + flag;
    getData(url, function(data){
        if(data == "success"){
            node.toggleClass("btn-danger");
            node.toggleClass("btn-success");
            if(node.hasClass("btn-danger")){
                sweetAlert("操作成功","成功添加好友","success");
                node.html("删除好友");
            }
            else{
                sweetAlert("操作成功","成功删除好友","success");
                node.html("加为好友");
            }
            
        }
        else if(data == "send"){
            sweetAlert("操作成功","好友请求发送成功!","success");
        }
        else{
            sweetAlert("出错啦","请求出错啦！","error");
        }
    });
});