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
      $("#matchModal .submit").on("click", {obj:node}, function(e){
            var val = $("input[name='team']:checked").val();
            if(!val) return;
            var node = e.data.obj;
              node.toggleClass("btn-success");
              node.toggleClass("btn-danger");
              node.html("退出比赛");
            $("#matchModal").modal("toggle");
            getData(URL + "&team=" + val,function(){});
      });  
      });
  }
});

var nodes = $(".col-xs-4");

for(var i = 0;i < nodes.length;i++){
    var ld = parseInt($(nodes[i].parentNode).attr("ld"));
    var gap = ld / 3;
    var width = "100%";
    if(ld - gap * 3 == 2)
        width = "50%";
    var node = $(nodes[i]);
    if(parseInt(node.attr("num")) / 3 <= gap)
       node.css({"width": "33.3%"});
    else
       node.css({"width": width});
}

$(function(){
	var fst = $('.list-group-item').get(1);
    $('.group-info').css('display','none');
	$(fst).next().css('display','block');
	$(fst).addClass('list-group-item-success');
	$('.list-group-item').click(function(e){
		$('.group-info').css('display','none');
		$('.list-group-item').removeClass('list-group-item-success');
		$(e.target).addClass('list-group-item-success');
		var tar = $(e.target).next();
		$(tar).css('display','block');
	});
});