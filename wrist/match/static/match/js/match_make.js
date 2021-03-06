$("#input_image").fileinput({
   language: "zh",
   uploadUrl: domain + "/data/match/make",
   allowedFileTypes: ["images"],
   maxFileSize: 5120,
   showUpload: false,
   showCaption: false,
   showCancel: true,
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

$("#tags input.form-control")[0].oninput = function(e){
    var node = $(e.target);
    var val = node.val();
    if(val.indexOf(' ') != -1){
        var content = val.substr(0, val.indexOf(' '));
        node.val('');
        $("#tags .extra").append("<div class='ui label'>" + content + "</div><input class='tags hide' name='tag" + $("input.tags.hide").length + "' value=" + content + " style='display: none'>");
    }
}

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
   var node = $("#tags .extra");
   node.append("<div class='ui label'>" + this.textContent + "</div><input class='tags hide' name='tag" + $("input.tags.hide").length + "' value=" + this.textContent + " style='display: none'>");
}

function friendClick(e){
   var node = $("#friends .extra");
   node.append("<div class='ui label'>" + this.textContent + "</div><input class='friends hide' name='friend" + $("input.friends.hide").length + "' value=" + this.textContent + " style='display: none'>");
}

function opponentClick(e){
   var node = $("#opponents .extra");
   node.append("<div class='ui label'>" + this.textContent + "</div><input class='opponents hide' name='opponent" + $("input.opponents.hide").length + "' value=" + this.textContent + " style='display: none'>");
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