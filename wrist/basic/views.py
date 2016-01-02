#-*- coding:utf-8 -*-

import random
import json
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from wechat import tools as wechat_tools
from models import User, DayData, Data, Good
from plan.models import Plan
from match.models import Match
import tools

# Create your views here.

def tmp(request):
    userId = request.session["userId"] = "ose6Ut8Ir-41wB7gQx89BifYa49Q"
    return HttpResponse(userId)

def redirect_profile(request):
    if not "userId" in request.session:
        return HttpResponseRedirect("/static/not_bind.html")
    try:
        page = int(request.GET["page"])
        userId = request.session["userId"]
        if page == 0:
            url = "today"
        elif page == 1:
            url = "rank"
        elif page == 2:
            url = "friend"
        elif page == 3:
            url = "profile"
        elif page == 4:
            url = "profile_other"
            userId = request.GET["userId"]
        url = "/static/basic/data_%s.html?%s" % (url, userId)
        return HttpResponseRedirect(url)
    except:
        return HttpResponseRedirect("/static/404.html")

def bind(request):
    request.session["userId"] = request.GET["openId"]
    return HttpResponseRedirect("/basic/profile?page=3")

def data_rank(request):
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
#    try:
    data = {}
    date = tools.getDate()
    users = User.objects.all()
    userId = data["userId"] = request.session["userId"]
    data["href"] = "%s/basic/redirect/profile" % wechat_tools.domain
    owner = User.objects.get(openId=userId)
    data["data_list"] = []
    num = 1
    for user in users:
        item = {}
        item["identity"] = 2
        if user.openId == userId:
            item["identity"] = 0
        else:
            flag = owner.friends.filter(openId=user.openId)
            if len(flag) > 0:
                item["identity"] = 1
        flag = Good.objects.filter(user=owner,type=0,target=user.id)
        if len(flag) > 0:
            item["isGood"] = 1
        item["userId"] = user.id
        item["num"] = 0
        item["username"] = user.name
        item["image"] = user.image
        dayData = DayData.objects.filter(user=user,date=date)
        if len(dayData) == 0:
            dayData = DayData(user=user,date=date)
            dayData.save()
        else:
            dayData = dayData[0]
        item["steps"] = dayData.steps
        item["goods"] = user.goods
        data["data_list"].append(item)
    data["data_list"] = sorted(data["data_list"], key=lambda user : user["steps"], reverse=True)
    ld = len(data["data_list"])
    for i in xrange(ld):
        data["data_list"][i]["num"] = i+1
 #   except:
 #       data = {"error": true}
    return HttpResponse(json.dumps(data), content_type="application/json")

def data_today(request):
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号页面绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
 #   try:  
    if not request.GET["userId"] == request.session["userId"]:
        data = {"error":{"title":u"权限问题","content":u"您无权访问此页面"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    data = {}
    date = tools.getDate()
    data["userId"] = userId = request.GET["userId"]
    data["href"] = "%s/basic/redirect/profile" % wechat_tools.domain
    user = User.objects.get(openId=userId)
    dayData = DayData.objects.filter(user=user,date=date)
    if len(dayData) == 0:
        dayData = DayData(user=user,date=date)
        dayData.save()
    else:
        dayData = dayData[0]
    data_list = Data.objects.filter(user=user,date=date)
    data["steps_now"] = dayData.steps
    data["steps_plan"] = user.dayPlan
    if data["steps_now"] < data["steps_plan"]:
        data["steps_per"] = data["steps_now"] * 100 / data["steps_plan"]
    else:
        data["steps_per"] = 100
    data["sleep_now_h"] = dayData.sleep / 60
    data["sleep_now_m"] = dayData.sleep % 60
    data["sleep_plan"] = user.sleepPlan
    if data["sleep_now_h"] < data["sleep_plan"]:
        data["sleep_per"] = int((data["sleep_now_h"] + float(data["sleep_now_m"]) / 60) * 100 / data["sleep_plan"])
    else:
        data["sleep_per"] = 100
    data["data_list"] = []
    for data_item in data_list:
        item = {}
        item["date"] = "%4d-%2d-%2d" % (date / 10000, date % 10000 / 100, date % 100)
        item["time"] = data_item.startTime.split(" ")[1][:5]
        type = data_item.type
        subType = data_item.subType
        item["content"] = tools.bong_activity[type-1][subType]
        data["data_list"].append(item)
 #   except:
 #       data = {}
 #       data["error"] = "true"
    return HttpResponse(json.dumps(data), content_type="application/json") 

def data_friend(request):
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号页面绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
 #   try:  
    if not request.GET["userId"] == request.session["userId"]:
        data = {"error":{"title":u"权限问题","content":u"您无权访问此页面"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    data = {}
    data["userId"] = userId = request.GET["userId"]
    data["href"] = "%s/basic/redirect/profile" % wechat_tools.domain
    user = User.objects.get(openId=userId)
    friends = user.friends.all()
    data["data_list"] = []
    for friend in friends:
        item = {}
        item["userId"] = friend.openId
        item["image"] = friend.image
        item["name"] = friend.name
        data["data_list"].append(item)
#    except:
    return HttpResponse(json.dumps(data), content_type="application/json")
    
def data_report(request):
    return render_to_response("basic/data_rank_.html", context_instance=RequestContext(request))

def data_good(request):
#    try:
        user = request.GET["user"]
        user = User.objects.get(openId=user)
        target = int(request.GET["target"])
        type = int(request.GET["type"])
        item = Good.objects.filter(user=user,target=target,type=type)
        if type == 0:
            tmp = User.objects.get(id=target)
        elif type == 1:
            tmp = Plan.objects.get(id=target)
        elif type == 2:
            tmp = Match.objects.get(id=target)
        goods = tmp.goods
        if len(item) == 0:
            item = Good(user=user,target=target,type=type)
            item.save()
            tmp.goods = goods + 1
        else:
            tmp.goods = goods - 1
            item[0].delete()
        tmp.save()
        return HttpResponse("success")
#    except:
#        return HttpResponse("error")

def data_profile(request):
    pass
