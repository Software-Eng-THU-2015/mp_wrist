$("#input_image").fileinput({
   language: "zh",
   uploadUrl: "http://wrist.ssast2015.com/data/match/make",
   allowedFileExtensions: ["jpg", "png"],
   showUpload: false,
   showCaption: false,
   browseClass: "btn btn-primary",
   previewFileIcon: "<i class='glyphicon glyphicon-king'></i>",
});

$(".form_datetime").datetimepicker({
   startDate: new Date(),
   format: "yyyy-mm-dd",
   autoclose: true,
   startView: 2,
   minView: 2,
   language: 'zh-CN'
});

$("body").click(function(){
    $(".btn-group .dropdown-menu").css({"display": "none"});
    $("#tag_add").click(function(e){
       $("#tags .btn-group .dropdown-menu").css({"display": "inline"});
       e.stopPropagation();
    });
    $("#friend_add").click(function(e){
       $("#friends .btn-group .dropdown-menu").css({"display": "inline"});
       e.stopPropagation();
    });
    $("#opponent_add").click(function(e){
       $("#opponents .btn-group .dropdown-menu").css({"display": "inline"});
       e.stopPropagation();
    });
    $("#tags .btn-group .dropdown-menu li").click(function(){
       $("tags input").val($("tags input").val() + "|" + $(this).html()); 
    });
    $("#friends .btn-group .dropdown-menu li").click(function(){
       $("#friends input").val($("#friends input").val() + "|" + $(this).html()); 
    });
    $("#opponents .btn-group .dropdown-menu li").click(function(){
       $("#oppenents input").val($("#friends input").val() + "|" + $(this).html()); 
    });
});