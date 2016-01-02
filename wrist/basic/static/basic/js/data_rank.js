var userId = $("#userId").attr("userId");

$('.heart.icon').click(function(){
    if($(this).hasClass("empty"))
        this.nextSibling.textContent = parseInt(this.nextSibling.textContent) + 1;
    else
        this.nextSibling.textContent = parseInt(this.nextSibling.textContent) - 1;
    $(this).toggleClass('empty');
    var xhr = new XMLHttpRequest();
    var URL = "http://wrist.ssast2015.com/basic/goods?type=0&user=" + userId + "&target=" + $(this).attr("userId");
    xhr.open("GET", URL, true);
    xhr.send(null);
});

$('.ui.progress').progress('reset');

var numberOne = parseInt($("#calories1").html());
var num = $(".ui .indicating .progress").length;
for(var i = 0;i < num;i++)
{
    $("#user" + (i+1)).progress({
       total: numberOne,
       value: parseInt($("#calories" + (i+1)).html())
    });
}