#-*- coding=utf-8 -*-

import tools

user = "ose6Ut8Ir-41wB7gQx89BifYa49Q"
menu = {
 "button":[
   {  
      "name":u"个人数据",
      "sub_button":[
      { 
        "type":"view",
        "name":u"绑定手环",
        "url":"http://wrist.ssast2015.com/basic/bind"
      },
	  {
		"type":"click",
		"name":u"今日战况",
		"key":"V1001_DATA_TODAY"
	  },
	  {
		"type":"click",
		"name":u"健康报告",
		"key":"V1001_DATA_REPORT"
	  },
	  {
		"type":"click",
		"name":u"排行榜",
		"key":"V1001_DATA_RANK"
	  }]
  },
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
		"name":u"查看我的",
		"key":"V1001_PLAN_OWN"
	  },
	  {
		"type":"click",
		"name":u"计划广场",
		"key":"V1001_PLAN_SHARE"
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
		"key":"V1001_MATCH_CREATE"
	  },
	  {
		"type":"click",
		"name":u"查看进度",
		"key":"V1001_MATCH_CHECK"
	  },
	  {
		"type":"click",
		"name":u"所有比赛",
		"key":"V1001_PLAN_SHOW"
	  }]
  }]
}

print tools.menuCreate(menu)