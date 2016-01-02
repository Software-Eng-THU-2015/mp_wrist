$("#input_image").fileinput({
   language: "zh",
   uploadUrl: domain + "/data/match/make",
   allowedFileExtensions: ["jpg", "png", "jpeg"],
   showUpload: false,
   showCaption: false,
   browseClass: "btn btn-primary",
   previewFileIcon: "<i class='glyphicon glyphicon-king'></i>",
});

$(".form_datetime").datetimepicker({
   startDate: new Date(),
   format: "yyyy-mm-dd hh:ii",
   autoclose: true,
   startView: 1,
   minView: 1,
   language: 'zh-CN'
});

var touch = ("ontouchstart" in window) || window.DocumentTouch && document instanceof DocumentTouch;

function bodyClick(e){
    $(".btn-group .dropdown-menu").css({"display": "none"});
}

function tagsClick(e){
   $(".btn-group .dropdown-menu").css({"display": "none"});
   $("#tags .btn-group .dropdown-menu").css({"display": "inline"});
   e.stopPropagation();
}

function friendsClick(e){
   $(".btn-group .dropdown-menu").css({"display": "none"});
   $("#friends .btn-group .dropdown-menu").css({"display": "inline"});
   e.stopPropagation();
}

function opponentsClick(e){
   $(".btn-group .dropdown-menu").css({"display": "none"});
   $("#opponents .btn-group .dropdown-menu").css({"display": "inline"});
   e.stopPropagation();
}

function tagClick(e){
   var node = $("#tags input");
   if(node.val() == "")
        node.val(this.textContent);
   else
        node.val(node.val() + "|" + this.textContent);
}

function friendClick(e){
   var node = $("#friends input");
   if(node.val() == "")
        node.val(this.textContent);
   else
        node.val(node.val() + "|" + this.textContent); 
}

function opponentClick(e){
   var node = $("#opponents input");
   if(node.val() == "")
        node.val(this.textContent);
   else
        node.val(node.val() + "|" + this.textContent); 
}

if(touch){
    $("body").on("touchstart", bodyClick);
    $("#tag_add").on("touchstart", tagsClick);
    $("#friend_add").on("touchstart", friendsClick);
    $("#opponent_add").on("touchstart", opponentsClick);
    $("#tags li").on("touchstart", tagClick);
    $("#friends li").on("touchstart", friendClick);
    $("#opponents li").on("touchstart", opponentClick);
}
else{
    $("body").on("click", bodyClick);
    $("#tag_add").on("click", tagsClick);
    $("#friend_add").on("click", friendsClick);
    $("#opponent_add").on("click", opponentsClick);
    $("#tags li").on("click", tagClick);
    $("#friends li").on("click", friendClick);
    $("#opponents li").on("click", opponentClick);
}