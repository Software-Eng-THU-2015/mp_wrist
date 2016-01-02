#-*- coding:utf-8 -*-

import random
import json
import time
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from basic.models import User, Good
from basic import tools as basic_tools
from wechat import tools as wechat_tools
from models import Plan, PTag
import tools

# Create your views here.

def redirect_plan(request):
    if not "userId" in request.session:
        return HttpResponseRedirect("/static/not_bind.html")
    page = int(request.GET["page"])
    if page == 0:
        url = "make"
    elif page == 1:
        url = "rank"
    elif page == 2:
        url = "square"
    elif page == 3:
        url = "own"
    elif page == 4:
        url = "rank"
    url = "/static/plan/plan_%s.html?%s" % (url, request.session["userId"])
    return HttpResponseRedirect(url)

def plan_make(request):
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if not request.GET["userId"] == request.session["userId"]:
        data = {"error":{"title":u"用户异常","content":u"请在公众号中制定自己的计划"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    data = {}
    userId = data["userId"] = request.GET["userId"]
    user = User.objects.get(openId=userId)
    data["href"] = "%s/plan/redirect" % wechat_tools.domain
    data["tags"] = []
    tags = PTag.objects.all()
    for tag in tags:
        data["tags"].append(tag.name)
    data["friends"] = []
    friends = user.friends.all()
    for friend in friends:
        item = {}
        item["name"] = friend.name
        item["image"] = friend.image
        data["friends"].append(item)
    return HttpResponse(json.dumps(data), content_type="application/json")
  
def plan_own(request):
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    data = {}
    userId = data["userId"] = request.GET["userId"]
    user = User.objects.get(openId=userId)
    data["href"] = "%s/plan/redirect" % wechat_tools.domain
    data["data_list"] = []
    plans = user.user_plan_owner.all()[:20]
    for plan in plans:
        item = {}
        item["createTime"] = basic_tools.getCreateTime(plan.createTime)
        item["title"] = plan.name
        item["description"] = plan.description
        item["image"] = plan.image
        item["tags"] = []
        tags = plan.plan_ptag_plans.all()
        for tag in tags:
            item["tags"].append(tag.name)
        tmp = Good.objects.filter(user=user,type=1,target=plan.id)
        if len(tmp) > 0:
            item["isGood"] = 1
        item["isFollow"] = 1
        data["data_list"].append(item)
    data["data_list"].reverse()
    return HttpResponse(json.dumps(data), content_type="application/json")

def plan_square(request):
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    data = {}
    userId = data["userId"] = request.session["userId"]
    user = User.objects.get(openId=userId)
    data["href"] = "%s/plan/redirect" % wechat_tools.domain
    data["data_list"] = []
    plans = Plan.objects.all()[:20]
    for plan in plans:
        item = {}
        item["user_image"] = plan.owner.image
        item["user_name"] = plan.owner.name
        item["createTime"] = basic_tools.getCreateTime(plan.createTime)
        item["title"] = plan.name
        item["description"] = plan.description
        item["image"] = plan.image
        item["tags"] = []
        tags = plan.plan_ptag_plans.all()
        for tag in tags:
            item["tags"].append(tag.name)
        tmp = Good.objects.filter(user=user,type=1,target=plan.id)
        if len(tmp) > 0:
            item["isGood"] = 1
        tmp = plan.members.filter(openId=userId)
        if len(tmp) > 0:
            item["isFollow"] = 1
        data["data_list"].append(item)
    data["data_list"].reverse()
    return HttpResponse(json.dumps(data), content_type="application/json")
            
@csrf_exempt
def submit_make(request):
    userId = request.POST["userId"]
    user = User.objects.get(openId=userId)
    now = int(time.time())
    plan = Plan(name=request.POST["plan_name"],description=request.POST["comment"],createTime=now,startTime="%s:00:00" % request.POST["begintime"],endTime="%s:00:00" % request.POST["endtime"],goal=request.POST["goal"],owner=user)
    plan.endDate, plan.endDateTime = basic_tools.splitDate(plan.endTime)
    prefix = "/data/www/wrist"
    path = "/media/plan/"
    if not os.path.exists(prefix+path):
        os.mkdir(prefix+path)
    file = request.FILES["image"]
    file_name = "%s%s_%s_%s" % (path, plan.name.encode("utf-8"), str(now), file.name.encode("utf-8"))
    des = open(prefix+file_name, "wb")
    for chunk in file.chunks():
        des.write(chunk)
    des.close()
    plan.image = file_name
    plan.save()
    tags = request.POST["tags"].split("|")
    for tag in tags:
        item = PTag.objects.filter(name=tag)
        if len(item) == 0:
            item = PTag(name=tag)
            item.save()
        else:
            item = item[0]
        item.plans.add(plan)
    return HttpResponseRedirect("/plan/redirect?page=4")
    
def plan_share(request):
#    try:
        userId = request.GET["userId"]
        user = User.objects.get(openId=userId)
        data = basic_tools.Object()
        data.userId = userId
        data.list = []
        plans = Plan.objects.all()
        for plan in plans:
            item = basic_tools.Object()
            item.userId = plan.id
            item.image = user.image
            item.plan_image = plan.images
            item.username = plan.owner.name
            item.createTime = tools.getCreateTime(plan.createTime)
            item.name = plan.name
            item.description = plan.description
            item.tags = []
            tags = plan.plan_ptag_plans.all()
            for tag in tags:
                item.tags.append(tag.name)
            tmp = Good.objects.filter(user=user,type=1,target=plan.id)
            if len(tmp) > 0:
                item.isLike = 1
            tmp = plan.members.filter(openId=user.openId)
            if len(tmp) > 0:
                item.isFollow = 1
            data.list.append(item)
        return render_to_response("plan/plan_share.html", {"data": data}, context_instance=RequestContext(request))
#    except:
#        return render_to_response("404.html")

def plan_rank(request):
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
#    try:
    data = {}
    userId = data["userId"] = request.session["userId"]
    user = User.objects.get(openId=userId)
    data["href"] = "%s/plan/redirect" % wechat_tools.domain
    data["data_list"] = []
    plans = Plan.objects.all()
    for plan in plans:
        item = {}
        item["id"] = plan.id
        item["num"] = 0
        item["user_image"] = plan.owner.image
        item["user_name"] = plan.owner.name
        item["image"] = plan.image
        item["title"] = plan.name
        item["description"] = plan.description
        item["tags"] = []
        tags = plan.plan_ptag_plans.all()
        for tag in tags:
            item["tags"].append(tag.name)
        item["goods"] = plan.goods
        tmp = plan.members.filter(openId=userId)
        if len(tmp) > 0:
            item["isFollow"] = 1
        data["data_list"].append(item)
    data["data_list"] = sorted(data["data_list"], key=lambda user : user["goods"], reverse=True)
    ld = len(data["data_list"])
    for i in xrange(ld):
        data["data_list"][i]["num"] = i+1
    return HttpResponse(json.dumps(data), content_type="application/json")
#    except:
#        return render_to_response("404.html")

def plan_follow(request):
    try:
        userId = request.GET["user"]
        user = User.objects.get(openId=userId)
        target = request.GET["target"]
        plan = Plan.objects.get(id=target)
        tmp = plan.members.filter(openId=userId)
        if len(tmp) == 0:
            plan.members.add(user)
        else:
            plan.members.remove(user)
        return HttpResponse("success")
    except:
        return HttpResponse("error")
