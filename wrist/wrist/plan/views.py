#-*- coding:utf-8 -*-

import random
from django.shortcuts import render_to_response
from django.template import RequestContext
from wechat import tools as wechat_tools
from basic.models import User
from basic import tools

# Create your views here.

def plan_make(request):
    if request.method == "GET":
        return render_to_response("plan/plan_make.html", context_instance=RequestContext(request))
    else:
        return render_to_response("plan/plan_make.html", context_instance=RequestContext(request))

def plan_own(request):
    return render_to_response("plan/plan_own.html", context_instance=RequestContext(request))

def plan_share(request):
    plans = []
    user = ["asd", "asfe", "zxwer", "asdxvt", "qweq"]
    tags = [u"瑜伽", u"排球", u"游泳", u"3km"]
    for i in xrange(5):
        plan = tools.Object()
        plan.user_img = "/static/basic/img/small/%d.jpg" % i
        plan.creator = user[i]
        plan.createTime = "1 Hour Ago"
        plan.title = u"我爱运动//我是计划标题"
        plan.content = u"我要跑步//我是计划详情"
        plan.img = ["/static/basic/img/share_%d.jpg" % (i % 2)]
        plan.tags = []
        for j in xrange(random.randint(1,3)):
            plan.tags.append(tags[random.randint(0,3)])
        plans.append(plan)
    return render_to_response("plan/plan_share.html", {"plans": plans}, context_instance=RequestContext(request))

def plan_rank(request):
    plans = []
    user = ["asd", "asfe", "zxwer", "asdxvt", "qweq"]
    tags = [u"瑜伽", u"排球", u"游泳", u"3km"]
    for i in xrange(5):
        plan = tools.Object()
        plan.id = 0
        plan.user_img = "/static/basic/img/small/%d.jpg" % i
        plan.username = user[i]
        plan.title = u"我爱运动//我是计划标题"
        plan.content = u"我要跑步//我是计划详情"
        plan.tags = []
        for j in xrange(random.randint(1,3)):
            plan.tags.append(tags[random.randint(0,3)])
        plan.goods = random.randint(0,10)
        plans.append(plan)
    plans = sorted(plans, key=lambda plan : plan.goods, reverse=True)
    for i in xrange(5):
        plans[i].id = i + 1
    return render_to_response("plan/plan_rank.html", {"plans": plans}, context_instance=RequestContext(request))
