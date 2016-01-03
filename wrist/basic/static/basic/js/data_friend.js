$(".userLink").click(function(){
    window.location.href = $(".link").attr("to") + "?page=4&id=" + $(this).attr("userId");
});