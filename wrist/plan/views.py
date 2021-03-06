#-*- coding:utf-8 -*-

import random
import json
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from basic.models import User, Good
from basic import tools as basic_tools
from wechat import tools as wechat_tools
from models import Plan, PTag, PlanProgress
import tools

# Create your views here.

def redirect_plan(request):
    try:
        if os.environ.get("TEST", None):
            request.session["userId"] = request.GET["userId"]
        if not "userId" in request.session:
            return HttpResponseRedirect("/static/not_bind.html")
        page = int(request.GET["page"])
        userId = request.session["userId"]
        if page == 0:
            url = "make"
        elif page == 1:
            url = "rank"
        elif page == 2:
            url = "square"
        elif page == 3:
            url = "own"
        elif page == 4:
            url = "profile"
            id = request.GET["id"]
            userId = "%s&%s" % (id, userId)
        url = "/static/plan/plan_%s.html?%s" % (url, userId)
        return HttpResponseRedirect(url)
    except:
        return HttpResponseRedirect("/static/404.html")

def plan_make(request):
    if os.environ.get("TEST", None):
        request.session["userId"] = request.GET["userId"]
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if not "userId" in request.GET:
        data = {"error":{"title":u"出错啦","content":u"这个页面找不到啦!"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if not request.GET["userId"] == request.session["userId"]:
        data = {"error":{"title":u"用户异常","content":u"请在公众号中制定自己的计划"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    try:
        data = {}
        userId = data["userId"] = request.GET["userId"]
        user = User.objects.get(openId=userId)
        data["href"] = "%s/plan/redirect/profile" % wechat_tools.domain
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
            item["userId"] = friend.openId
            data["friends"].append(item)
    except:
        data = {"error":{"title":u"出错啦","content":u"页面找不到啦!"}}
    return HttpResponse(json.dumps(data), content_type="application/json")
  
def plan_own(request):
    if os.environ.get("TEST", None):
        request.session["userId"] = request.GET["userId"]
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if not "userId" in request.GET:
        data = {"error":{"title":u"出错啦","content":u"这个页面找不到啦!"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    try:
        data = {}
        ownerId = data["userId"] = request.session["userId"]
        userId = request.GET["userId"]
        user = User.objects.get(openId=userId)
        data["href"] = "%s/plan/redirect/profile" % wechat_tools.domain
        data["data_list"] = []
        ld = user.user_plan_members.all().count()
        if ld < 20:
            ld = 20
        plans = user.user_plan_members.all()[ld-20:]
        for plan in plans:
            item = {}
            item["id"] = plan.id
            item["createTime"] = basic_tools.getCreateTime(plan.createTime)
            item["title"] = plan.name
            item["description"] = plan.description
            item["image"] = plan.image
            item["goods"] = plan.goods
            item["tags"] = []
            tags = plan.plan_ptag_plans.all()
            for tag in tags:
                item["tags"].append(tag.name)
            item["isFollow"] = 1
            if plan.finished == 1:
                item["isFinished"] = 1
            data["data_list"].append(item)
        data["data_list"].reverse()
    except:
        data = {"error":{"title":u"出错啦","content":u"页面找不到啦!"}}
    return HttpResponse(json.dumps(data), content_type="application/json")

def plan_square(request):
    if os.environ.get("TEST", None):
        request.session["userId"] = request.GET["userId"]
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if not "userId" in request.GET:
        data = {"error":{"title":u"出错啦","content":u"这个页面找不到啦!"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    try:
        data = {}
        userId = data["userId"] = request.session["userId"]
        user = User.objects.get(openId=userId)
        data["href"] = "%s/plan/redirect/profile" % wechat_tools.domain
        data["data_list"] = []
        ld = Plan.objects.all().count()
        if ld < 20:
            ld = 20
        plans = Plan.objects.all()[ld-20:]
        for plan in plans:
            item = {}
            item["id"] = plan.id
            item["user_image"] = plan.owner.image
            item["user_name"] = plan.owner.name
            item["createTime"] = basic_tools.getCreateTime(plan.createTime)
            item["title"] = plan.name
            item["description"] = plan.description
            item["image"] = plan.image
            item["goods"] = plan.goods
            item["tags"] = []
            tags = plan.plan_ptag_plans.all()
            for tag in tags:
                item["tags"].append(tag.name)
            tmp = plan.members.filter(openId=userId).count()
            if tmp > 0:
                item["isFollow"] = 1
            if plan.finished == 1:
                item["isFinished"] = 1
            data["data_list"].append(item)
        data["data_list"].reverse()
    except:
        data = {"error":{"title":u"出错啦","content":u"页面找不到啦!"}}
    return HttpResponse(json.dumps(data), content_type="application/json")
            
@csrf_exempt
def submit_make(request):
    if os.environ.get("TEST", None):
        request.session["userId"] = request.GET["userId"]
    if not "userId" in request.session:
        return HttpResponseRedirect("/static/not_bind.html")
    if not "userId" in request.POST:
        return HttpResponseRedirect("/static/404.html")
    if not request.POST["userId"] == request.session["userId"]:
        return HttpResponseRedirect("/static/404.html")
    try:
        userId = request.POST["userId"]
        user = User.objects.get(openId=userId)
        now = basic_tools.getNow()
        plan = Plan(name=request.POST["plan_name"],description=request.POST["comment"],createTime=now,startTime=basic_tools.DateToInt("%s:00:00" % request.POST["begintime"][:13]),endTime=basic_tools.DateToInt("%s:00:00" % request.POST["endtime"][:13]),owner=user)
        if request.POST["goal"] == "":
            goal = 0
        else:
            goal = int(request.POST["goal"])
        plan.goal=goal
        plan.save()
        if goal > 0:
            progress = PlanProgress(plan=plan,user=user)
            progress.save()
        tags = []
        tag = request.POST["tags"]
        if not tag == "":
            item = PTag.objects.filter(name=tag)
            if len(item) == 0:
                item = PTag(name=tag)
                item.save()
            else:
                item = item[0]
            if not item.plans.filter(id=plan.id).exists():
                tags.append(tag)
                item.plans.add(plan)
        i = 0
        while ("tag%d" % i) in request.POST:
            tag = request.POST["tag%d" % i]
            i += 1
            if not tag == "":
                item = PTag.objects.filter(name=tag)
                if len(item) == 0:
                    item = PTag(name=tag)
                    item.save()
                else:
                    item = item[0]
                if not item.plans.filter(id=plan.id).exists():
                    tags.append(tag)
                    item.plans.add(plan)
        if len(tags) == 0 and goal > 0:
            tag = "%d步" % goal
            item = PTag.objects.filter(name=tag)
            if len(item) == 0:
                item = PTag(name=tag)
                item.save()
            else:
                item = item[0]
            if not item.plans.filter(id=plan.id).exists():
                tags.append(tag)
                item.plans.add(plan)
        prefix = os.environ.get("WRIST_HOME")
        path = "/media/plan/"
        if not os.path.exists(prefix+path):
            os.mkdir(prefix+path)
        if "image" in request.FILES:
            file = request.FILES["image"]
            file_name = "%s%s_%s_%s" % (path, plan.name.encode("utf-8"), str(now), file.name.encode("utf-8"))
            des = open(prefix+file_name, "wb")
            for chunk in file.chunks():
                des.write(chunk)
            des.close()
        else:
            file_name = tools.getDefaultImageByTag(tags)
        plan.image = file_name
        plan.save()
        plan.members.add(user)
        i = 0
        while ("friend%d" % i) in request.POST:
            tools.sendInvite(user, plan.id, request.POST["friend%d" % i])
            i += 1
        return HttpResponseRedirect("/plan/redirect/profile?page=4&id=%d" % plan.id)
    except:
        return HttpResponseRedirect("/static/404.html")

def plan_rank(request):
    if os.environ.get("TEST", None):
        request.session["userId"] = request.GET["userId"]
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if not "userId" in request.GET:
        data = {"error":{"title":u"出错啦","content":u"这个页面找不到啦!"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    try:
        data = {}
        userId = data["userId"] = request.session["userId"]
        user = User.objects.get(openId=userId)
        data["href"] = "%s/plan/redirect/profile" % wechat_tools.domain
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
            if plan.finished == 1:
                item["isFinished"] = 1
            data["data_list"].append(item)
        data["data_list"] = sorted(data["data_list"], key=lambda user : user["goods"], reverse=True)
        ld = len(data["data_list"])
        for i in xrange(ld):
            data["data_list"][i]["num"] = i+1
    except:
        data = {"error":{"title":u"出错啦","content":u"页面找不到啦!"}}
    return HttpResponse(json.dumps(data), content_type="application/json")

def plan_follow(request):
    if os.environ.get("TEST", None):
        request.session["userId"] = request.GET["user"]
    if not "userId" in request.session:
        return HttpResponse("error")
    if not "user" in request.GET:
        return HttpResponse("error")
    if not request.GET["user"] == request.session["userId"]:
        return HttpResponse("error")
    try:
        userId = request.GET["user"]
        user = User.objects.get(openId=userId)
        target = request.GET["target"]
        plan = Plan.objects.get(id=target)
        tmp = plan.members.filter(openId=userId).count()
        if tmp == 0:
            plan.members.add(user)
            progress = PlanProgress(plan=plan,user=user)
            progress.save()
        else:
            plan.members.remove(user)
            PlanProgress.objects.filter(plan=plan,user=user).delete()
        return HttpResponse("success")
    except:
        return HttpResponse("error")
        
def plan_profile(request):
    if os.environ.get("TEST", None):
        request.session["userId"] = request.GET["userId"]
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if not "userId" in request.GET:
        data = {"error":{"title":u"出错啦","content":u"这个页面找不到啦!"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    try:
        data = {}
        userId = data["userId"] = request.session["userId"]
        user = User.objects.get(openId=userId)
        data["href"] = "%s/plan/redirect/profile" % wechat_tools.domain
        id = request.GET["id"]
        plan = Plan.objects.get(id=id)
        data["image"] = plan.image
        data["title"] = plan.name
        data["startTime"] = basic_tools.IntToDate(plan.startTime)
        data["endTime"] = basic_tools.IntToDate(plan.endTime)
        data["description"] = plan.description
        data["goods"] = plan.goods
        data["id"] = plan.id
        if not plan.goal == 0:
            data["goal"] = plan.goal
            data["progress_value"] = tools.getProgress(plan, user)
        tags = plan.plan_ptag_plans.all()
        data["tags"] = []
        for tag in tags:
            data["tags"].append(tag.name)
        if Good.objects.filter(user=user,type=1,target=plan.id).count() > 0:
            data["isGood"] = 1
        tmp = plan.members.filter(openId=userId).count()
        if tmp > 0:
            data["isFollow"] = 1
        if plan.finished == 1:
            data["isFinished"] = 1
    except:
        data = {"error":{"title":u"出错啦","content":u"页面找不到啦!"}}
    return HttpResponse(json.dumps(data), content_type="application/json")