var userId = $("#userId").attr("userId");

$(".profileLink").click(function(){
    window.location.href = $(".link").attr("to") + "?page=3&id=" + $(this).attr("userId");
});

$('.follow.button').click(function(){
  var node = $(this);
  var URL = domain + "/match/join?userId=" + userId + "&target=" + $(this).attr("userId");
  if(node.hasClass('blue')){
      getData(URL, function(data){
          if(data == "delete")
              $(this.parentNode.parentNode.parentNode).css({"display":"none"});
      });
      $(this).html('<i class="paw icon"></i>&nbsp&nbsp&nbsp&nbspJoin&nbsp&nbsp&nbsp');
      node.toggleClass('blue');
  }
  else{
      var tpl = $(".template").html();
      var template = Handlebars.compile(tpl);
      getData(URL.replace("join","list"), function(data){
      var json = eval("(" + data + ")");
      $(".tip").html(template(json));
      $("#matchModal").modal("show");
      $("#matchModal .submit").on("click", {obj:node}, function(e){
            var val = $("input[name='team']:checked").val();
            if(!val) return;
            var node = e.data.obj;
            console.log(node);
            node.html('<i class="paw icon"></i>Joined');
            node.toggleClass('blue');
            $("#matchModal").modal("toggle");
            getData(URL + "&team=" + val,function(){});
      });  
      });
  }
});

