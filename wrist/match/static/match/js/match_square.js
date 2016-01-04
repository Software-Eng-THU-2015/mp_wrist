var userId = $("#userId").attr("userId");

$('.follow.button').click(function(){
  var node = $(this);
  var URL = domain + "/match/join?userId=" + userId + "&target=" + $(this).attr("userId");
  if(node.hasClass('blue')){
      getData(URL, function(){});
      $(this).html('<i class="paw icon"></i>&nbsp&nbsp&nbsp&nbspJoin&nbsp&nbsp&nbsp');
      node.toggleClass('blue');
  }
  else{
      var tpl = $($(".template")[1]).html();
      var template = Handlebars.compile(tpl);
      getData(URL.replace("join","list"), function(data){
      $(".tip").html(template(data));
      $("#matchModal").modal("show");
      $("#matchModal .submit").on("click", {obj:this}, function(e){
            var val = $("input[name='team']:checked").val();
            if(!val) return;
            var node = $(e.data.obj);
            node.html('<i class="paw icon"></i>Joined');
            node.toggleClass('blue');
            $("#matchModal").modal("toggle");
            getData(URL + "&team=" + val);
      });  
      }
  }
});

