var userId = $("#userId").attr("userId");

$('.heart.icon').click(function(){
    if($(this).hasClass("empty"))
        this.nextSibling.textContent = parseInt(this.nextSibling.textContent) + 1;
    else
        this.nextSibling.textContent = parseInt(this.nextSibling.textContent) - 1;
    $(this).toggleClass('empty');
    var xhr = new XMLHttpRequest();
    var URL = domain + "/basic/data/goods?type=0&user=" + userId + "&target=" + $(this).attr("userId");
    xhr.open("GET", URL, true);
    xhr.send(null);
});

$(".profileLink").click(function(){
   window.location.href = $(".link").attr("to") + "?page=4&id=" + $(this).attr("userId"); 
});

$('.ui.progress').progress('reset');

var numberOne = parseInt($("#step1").html());
var num = $(".ui.indicating.progress").length;
for(var i = 0;i < num;i++)
{
    $("#user" + (i+1)).progress({
       total: numberOne,
       value: parseInt($("#step" + (i+1)).html())
    });
}