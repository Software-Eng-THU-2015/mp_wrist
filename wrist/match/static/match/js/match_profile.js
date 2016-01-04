var userId = $("#userId").attr("userId");

$('.follow.button').click(function(){
  var node = $(this);
  var URL = domain + "/match/join?userId=" + userId + "&target=" + $(this).attr("userId");
  if(node.hasClass('btn-success')){
      getData(URL, function(){});
      node.toggleClass("btn-success");
      node.toggleClass("btn-danger");
      node.html("加入比赛");
  }
  else{
      var tpl = $(".template").html();
      var template = Handlebars.compile(tpl);
      getData(URL.replace("join","list"), function(data){
      var json = eval("(" + data + ")");
      $(".tip").html(template(json));
      $("#matchModal").modal("show");
      $("#matchModal .submit").on("click", {obj:this}, function(e){
            var val = $("input[name='team']:checked").val();
            if(!val) return;
            var node = $(e.data.obj);
              node.toggleClass("btn-success");
              node.toggleClass("btn-danger");
              node.html("退出比赛");
            $("#matchModal").modal("toggle");
            getData(URL + "&team=" + val);
      });  
      });
  }
});

