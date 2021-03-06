#-*- coding:utf-8 -*-

import os
import random
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from wechat import tools as wechat_tools
from models import User, DayData, Data, Good, Archive, PreFriend
from plan.models import Plan
from match.models import Match
from match import tools as match_tools
import tools

# Create your views here.

def get_session(request):
    if "userId" in request.GET:
        userId = request.session["userId"] = request.GET["userId"]
    else:
        userId = request.session["userId"] = "ose6Ut8Ir-41wB7gQx89BifYa49Q"
    return HttpResponse(userId)

def redirect_profile(request):
    if os.environ.get("TEST", None):
        request.session["userId"] = request.GET["userId"]
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
            userId = request.GET["id"]
        url = "/static/basic/data_%s.html?%s" % (url, userId)
        return HttpResponseRedirect(url)
    except:
        return HttpResponseRedirect("/static/404.html")

@csrf_exempt
def bind(request):
    if request.method == "POST":
        return HttpResponseRedirect("/basic/redirect/profile?page=3")
    else:
        request.session["userId"] = request.GET["openId"]
        return HttpResponseRedirect("/static/basic/data_bind.html")

def data_rank(request):
    if os.environ.get("TEST", None):
        request.session["userId"] = request.GET["userId"]
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    try:
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
            item["userId"] = user.openId
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
    except:
        data = {"error":{"title":u"出错啦","content":u"页面找不到啦!"}}
    return HttpResponse(json.dumps(data), content_type="application/json")

def data_today(request):
    if os.environ.get("TEST", None):
        request.session["userId"] = request.GET["userId"]
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号页面绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    try:  
        if not request.GET["userId"] == request.session["userId"]:
            data = {"error":{"title":u"权限问题","content":u"您无权访问此页面"}}
            return HttpResponse(json.dumps(data), content_type="application/json")
        data = {}
        date = tools.getDate()
        data["userId"] = userId = request.session["userId"]
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
    except:
        data = {"error":{"title":u"出错啦","content":u"页面找不到啦!"}}
    return HttpResponse(json.dumps(data), content_type="application/json") 

def data_friend(request):
    if os.environ.get("TEST", None):
        request.session["userId"] = request.GET["userId"]
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号页面绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    try:  
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
    except:
        data = {"error":{"title":u"出错啦","content":u"页面找不到啦!"}}  
    return HttpResponse(json.dumps(data), content_type="application/json")

def data_good(request):
    if os.environ.get("TEST", None):
        request.session["userId"] = request.GET["userId"]
    try:
        if not "userId" in request.session:
            return HttpResponse("error")
        if not "user" in request.GET:
            return HttpResponse("error")
        if not request.GET["user"] == request.session["userId"]:
            return HttpResponse("error")
        user = request.GET["user"]
        user = User.objects.get(openId=user)
        target = int(request.GET["target"])
        type = int(request.GET["type"])
        item = Good.objects.filter(user=user,target=target,type=type)
        if type == 0:
            tmp = User.objects.get(id=target)
        elif type == 1:
            tmp = Plan.objects.get(id=target)
        goods = tmp.goods
        if item.count() == 0:
            item = Good(user=user,target=target,type=type)
            item.save()
            tmp.goods = goods + 1
        else:
            tmp.goods = goods - 1
            item[0].delete()
        tmp.save()
        return HttpResponse("success")
    except:
        return HttpResponse("error")

def data_profile(request):
    if os.environ.get("TEST", None):
        request.session["userId"] = request.GET["userId"]
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号页面绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if not "userId" in request.GET:
        data = {"error":{"title":u"出错啦","content":u"这个页面找不到啦!"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    try:
        flag = request.GET["userId"] == request.session["userId"]
        data = {}
        data["userId"] = ownerId = request.session["userId"]
        userId = request.GET["userId"]
        data["href"] = "%s/basic/redirect/profile" % wechat_tools.domain
        user = User.objects.get(openId=userId)
        data["image"] = user.image
        data["name"] = user.name
        data["level"] = user.level
        data["height"] = user.height
        data["weight"] = user.weight
        data["dayPlan"] = user.dayPlan
        data["sleepPlan"] = user.sleepPlan
        data["archives"] = []
        archives = user.user_archive_owners.all()
        for archive in archives:
            data["archives"].append(archive.name)
        data["data_report"] = [
        {"period":[{"type_text":u"日步数","nav_step":True,"type":"Days","nav_day":True},{"type_text":u"周步数","nav_step":True,"type":"Weeks","nav_week":True},{"type_text":u"月步数","nav_step":True,"type":"Months","nav_month":True}],"type":"Step","num":1},
        {"period":[{"type_text":u"日热量","nav_calories":True,"type":"Days","nav_day":True},{"type_text":u"周热量","nav_calories":True,"type":"Weeks","nav_week":True},{"type_text":u"月热量","nav_calories":True,"type":"Months","nav_month":True}],"type":"Cal","num":2},
        {"period":[{"type_text":u"日距离","nav_distance":True,"type":"Days","nav_day":True},{"type_text":u"周距离","nav_distance":True,"type":"Weeks","nav_week":True},{"type_text":u"月距离","nav_distance":True,"type":"Months","nav_month":True}],"type":"Dis","num":3},
        {"period":[{"type_text":u"日睡眠","nav_sleep":True,"type":"Days","nav_day":True},{"type_text":u"周睡眠","nav_sleep":True,"type":"Weeks","nav_week":True},{"type_text":u"月睡眠","nav_sleep":True,"type":"Months","nav_month":True}],"type":"Sleep","num":4},
        ]
        data["report"] = user.comment
        data["chart_data"] = {"day":[],"week":[],"month":[]}
        date = tools.getDate()
        for i in xrange(7):
            item = DayData.objects.filter(user=user,date=date)
            if len(item) == 0:
                break
            item = item[0]
            it = {}
            it["date"] = tools.DateToStr(date)
            it["step_value"] = item.steps
            it["step_object"] = item.steps_goal
            it["cal_value"] = item.calories
            it["cal_object"] = item.calories_goal
            it["dis_value"] = item.distance
            it["dis_object"] = item.distance_goal
            it["sleep_value"] = item.sleep
            it["sleep_object"] = item.sleep_goal
            data["chart_data"]["day"].append(it)
            date = tools.getPreDate(date)
        data["chart_data"]["day"].reverse()
        date = tools.getDate()
        for i in xrange(4):
            item = DayData.objects.filter(user=user,date=date)
            if len(item) == 0:
                break
            it = {}
            it["date"] = tools.DateToStr(date)
            step_value = step_object = cal_value = cal_object = dis_value = dis_object = sleep_value = sleep_object = 0
            for j in xrange(7):
                item = item[0]
                step_value += item.steps
                step_object += item.steps_goal
                cal_value += item.calories
                cal_object += item.calories_goal
                dis_value += item.distance
                dis_object += item.distance_goal
                sleep_value += item.sleep
                sleep_object += item.sleep_goal
                date = tools.getPreDate(date)
                item = DayData.objects.filter(user=user,date=date)
                if len(item) == 0:
                    item = None
                    break
            it["step_value"] = step_value
            it["step_object"] = step_object
            it["cal_value"] = cal_value
            it["cal_object"] = cal_object
            it["dis_value"] = dis_value
            it["dis_object"] = dis_object
            it["sleep_value"] = sleep_value
            it["sleep_object"] = sleep_object
            data["chart_data"]["week"].append(it)
            if not item:
                break
        data["chart_data"]["week"].reverse()
        date = tools.getDate()
        year = date / 10000
        month = date % 10000 / 100
        day = date % 100
        for i in xrange(3):
            date = year * 10000 + month * 100 + day
            item = DayData.objects.filter(user=user,date=date)
            if len(item) == 0:
                break
            it = {}
            step_value = step_object = cal_value = cal_object = dis_value = dis_object = sleep_value = sleep_object = 0
            it["date"] = "%04d-%02d" % (year, month)
            for j in xrange(day):
                date = year * 10000 + month * 100 + day - j
                item = DayData.objects.filter(user=user,date=date)
                if len(item) == 0:
                    item = None
                    break
                item = item[0]
                step_value += item.steps
                step_object += item.steps_goal
                cal_value += item.calories
                cal_object += item.calories_goal
                dis_value += item.distance
                dis_object += item.distance_goal
                sleep_value += item.sleep
                sleep_object += item.sleep_goal
            it["step_value"] = step_value
            it["step_object"] = step_object
            it["cal_value"] = cal_value
            it["cal_object"] = cal_object
            it["dis_value"] = dis_value
            it["dis_object"] = dis_object
            it["sleep_value"] = sleep_value
            it["sleep_object"] = sleep_object
            data["chart_data"]["month"].append(it)
            if not item:
                break
        data["chart_data"]["month"].reverse()
        data["chart_data"] = json.dumps(data["chart_data"])
        if not flag:
            data["plans"] = []
            ld = user.user_plan_members.all().count()
            if ld < 3:
                ld = 3
            plans = user.user_plan_members.all()[ld-3:]
            for plan in plans:
                item = {}
                item["name"] = plan.name
                item["id"] = plan.id
                item["tags"] = []
                tags = plan.plan_ptag_plans.all()[:3]
                for tag in tags:
                    item["tags"].append(tag.name)
                data["plans"].append(item)
            data["matchs"] = []
            ld = user.user_match_members.all().count()
            if ld < 3:
                ld = 3
            matchs = user.user_match_members.all()[ld-3:]
            for match in matchs:
                item = {}
                item["name"] = match.title
                item["id"] = match.id
                item["tags"] = []
                tags = match.match_mtag_matchs.all()[:3]
                for tag in tags:
                    item["tags"].append(tag.name)
                data["matchs"].append(item)
            tmp = user.friends.filter(openId=ownerId)
            if len(tmp) > 0:
                data["isFriend"] = 1
            data["id"] = userId
    except:
        data = {"error":{"title":u"出错啦","content":u"页面找不到啦!"}}
    return HttpResponse(json.dumps(data), content_type="application/json")
    
def friend_add(request):
    if os.environ.get("TEST", None):
        request.session["userId"] = request.GET["userId"]
    try:
        if not "userId" in request.session:
            return HttpResponse("error")
        if not "userId" in request.GET:
            return HttpResponse("error")
        if not request.GET["userId"] == request.session["userId"]:
            return HttpResponse("error")
        result = "success"
        userId = request.GET["userId"]
        user = User.objects.get(openId=userId)
        id = request.GET["target"]
        type = int(request.GET["type"])
        if type == 0:
            target = User.objects.get(openId=id)
            preFriend = PreFriend.objects.filter(user=target,target=user)
            if preFriend.count() > 0:
                user.friends.add(target)
                target.friends.add(user)
                preFriend.delete()
            else:
                url = "%s/basic/redirect/profile?page=4&id=%s" % (wechat_tools.domain, userId)
                data = {
                  "title":{
                   "value":u"好友请求",
                   "color":"#000000",
                  },
                  "content":{
                   "value":u"%s想要加您为好友" % user.name,
                   "color":"#007fff",
                  },
                  "remark":{
                   "value":u"点击查看对方信息",
                   "color":"#666666"
                  }
                }
                wechat_tools.customSendTemplate(id, wechat_tools.template_id["msg"], "#000000", data, url)
                tmp = PreFriend(user=user,target=target)
                tmp.save()
                result = "send"
        else:
            target = user.friend.filter(openId=id)
            user.friends.remove(target)
            target.friends.remove(user)
            url = "%s/basic/redirect/profile?page=4&id=%s" % (wechat_tools.domain, userId)
            data = {
              "title":{
               "value":u"取消好友",
               "color":"#000000",
              },
              "content":{
               "value":u"%s取消了好友关系" % user.name,
               "color":"#007fff",
              },
              "remark":{
               "value":u"点击查看对方信息",
               "color":"#666666"
              }
            }
            wechat_tools.customSendTemplate(id, wechat_tools.template_id["msg"], "#000000", data, url)
        return HttpResponse(result)
    except:
        return HttpResponse("error")

def profile_data(request):
    if os.environ.get("TEST", None):
        request.session["userId"] = request.GET["userId"]
    if not "userId" in request.session:
        return HttpResponse("error")
    if not "userId" in request.GET:
        return HttpResponse("error")
    if not request.GET["userId"] == request.session["userId"]:
        return HttpResponse("error")
    try:
        userId = request.GET["userId"]
        type = int(request.GET["type"])
        value = int(request.GET["value"])
        user = User.objects.get(openId=userId)
        if type == 0:
            user.height = value
        elif type == 1:
            user.weight = value
        elif type == 2:
            user.dayPlan = value
            dayData = DayData.objects.get(user=user,date=tools.getDate())
            dayData.steps_goal = value
            h = user.height
            w = user.weight
            dayData.distance_goal = tools.stepToDis(value, h, w)
            dayData.calories_goal = tools.stepToCalories(value, h, w)
            dayData.save()
        elif type == 3:
            user.sleepPlan = value
            dayData = DayData.objects.get(user=user,date=tools.getDate())
            dayData.sleep_goal = value
            dayData.save()
        user.save()
        return HttpResponse("success")
    except:
        return HttpResponse("error")