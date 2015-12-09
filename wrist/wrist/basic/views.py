#-*- coding:utf-8 -*-

import random
from django.shortcuts import render_to_response
from django.template import RequestContext
from wechat import tools as wechat_tools
from models import User
import tools

# Create your views here.

def data_rank(request):
    users = User.objects.all()
    userlist = []
    num = 1
    for user in users:
        item = tools.Object()
        item.id = 0
        item.name = user.name
        item.image = user.image
        item.calories = tools.today_Calories(user.openId)
        item.goods = user.goods
        item.per = 0
        userlist.append(item)
    userlist = sorted(userlist, key=lambda user : user.calories, reverse=True)
    ld = len(userlist)
    for i in xrange(ld):
        userlist[i].id = i+1
        userlist[i].per = int(100 * userlist[i].calories / userlist[0].calories)
    return render_to_response("basic/data_rank.html", {"peoples": userlist}, context_instance=RequestContext(request))

def data_today(request):
    data = tools.Object()
    data.real_step = 231
    data.plan_step = 5000
    data.plan_per = int(100 * data.real_step / data.plan_step)
    data.calories = 123
    data.rank = 3
    data.list = []
    item = tools.Object()
    item.title = "sport"
    item.content = "run"
    item.startTime = "16:50"
    data.list.append(item)
    return render_to_response("basic/data_today.html", {"data": data}, context_instance=RequestContext(request))

def data_report(request):
    return render_to_response("basic/data_report.html", context_instance=RequestContext(request))

