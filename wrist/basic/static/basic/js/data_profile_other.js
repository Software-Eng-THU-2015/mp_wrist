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
    var url = domain + "/basic/add/friend?userId=" + userId + "&target=" + node.attr("userId") + "&type=" + str(flag);
    getData(url, function(data){
        if(data == "success"){
            node.toggleClass("btn-danger");
            node.toggleClass("btn-success");
            if(node.hasClass("btn-danger")){
                sweetAlert("�����ɹ�","�ɹ���Ӻ���","success");
                node.html("ɾ������");
            }
            else{
                sweetAlert("�����ɹ�","�ɹ�ɾ������","success");
                node.html("��Ϊ����");
            }
            
        }
        else if(data == "send"){
            sweetAlert("�����ɹ�","���������ͳɹ�!","success");
        }
        else{
            sweetAlert("������","�����������","error");
        }
    });
});