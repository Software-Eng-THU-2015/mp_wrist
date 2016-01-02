#-*- coding=utf-8 -*-

import tools

user = "ose6Ut8Ir-41wB7gQx89BifYa49Q"
menu = ""

tmp_id = "Ol_wljfNXMY3mrjJ0bQZbtPkouEYmVwm3y_jnO7MIMY"
data = {
   "content":{
     "value": u"我是内容",
     "color": "#173177"
   },
   "remark":{
     "value": u"",
     "color": "#007fff"
   }
}

menu = {
 "button":[
  {
      "name":u"运动计划",
      "sub_button":[
	  {
		"type":"click",
		"name":u"制定计划",
		"key":"V1001_PLAN_MAKE"
	  },
	  {
		"type":"click",
		"name":u"我的计划",
		"key":"V1001_PLAN_OWN"
	  },
	  {
		"type":"click",
		"name":u"计划广场",
		"key":"V1001_PLAN_SQUARE"
	  },
	  {
		"type":"click",
		"name":u"排行榜",
		"key":"V1001_PLAN_RANK"
	  }]
   },
   {
      "name":u"激情比赛",
      "sub_button":[
	  {
		"type":"click",
		"name":u"创建比赛",
		"key":"V1001_MATCH_MAKE"
	  },
	  {
		"type":"click",
		"name":u"查看进度",
		"key":"V1001_MATCH_CHECK"
	  },
	  {
		"type":"click",
		"name":u"比赛广场",
		"key":"V1001_MATCH_SQUARE"
	  }]
   },
   {  
      "name":u"个人中心",
      "sub_button":[
	  {
		"type":"click",
	    "name":u"绑定手环",
		"key":"V1001_DATA_BIND"
      },
	  {
		"type":"click",
		"name":u"今日战况",
		"key":"V1001_DATA_TODAY"
	  },
	  {
		"type":"click",
		"name":u"个人中心",
		"key":"V1001_DATA_PROFILE"
	  },
	  {
		"type":"click",
		"name":u"帮助",
		"key":"V1001_DATA_HELP"
       }]
  }]
}

print tools.menuCreate(menu)
