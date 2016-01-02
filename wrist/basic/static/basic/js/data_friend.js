$(".userLink").click(function(){
    window.location.href = $(".link").attr("to") + "?page=4&userId=" + $(this).attr("userId");
});