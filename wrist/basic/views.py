#-*- coding:utf-8 -*-

import random
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from wechat import tools as wechat_tools
from models import User, DayData, Data, Good, Archive
from plan.models import Plan
from match.models import Match
from match import tools as match_tools
import tools

# Create your views here.

def get_session(request):
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
            userId = request.GET["id"]
        url = "/static/basic/data_%s.html?%s" % (url, userId)
        return HttpResponseRedirect(url)
    except:
        return HttpResponseRedirect("/static/404.html")

def bind(request):
    if request.method == "POST":
        return HttpResponseRedirect("/basic/profile?page=3")
    else:
        request.session["userId"] = request.GET["openId"]
        return HttpResponseRedirect("/static/basic/data_bind.html")

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
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号页面绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if not "userId" in request.GET:
        data = {"error":{"title":u"出错啦","content":u"这个页面找不到啦!"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    flag = request.GET["userId"] == request.session["userId"]
    data = {}
    data["userId"] = ownerId = request.session["userId"]
    userId = request.GET["userId"]
    data["href"] = "%s/basic/redirect/profile" % wechat_tools.domain
    user = User.objects.get(openId=userId)
    data["image"] = user.image
    data["name"] = user.name
    data["level"] = user.level
    data["archives"] = []
    archives = user.user_archive_owners.all()
    for archive in archives:
        data["archives"].append(archive.name)
    data["data_report"] = [
    {"period":[{"type_text":u"日步数","nav_step":True,"type":"Days"},{"type_text":u"周步数","nav_step":True,"type":"Weeks"},{"type_text":u"月步数","nav_step":True,"type":"Months"}],
    "type":"Step","num":1},
    {"period":[{"type_text":u"日热量","nav_calories":True,"type":"Days"},{"type_text":u"周热量","nav_calories":True,"type":"Weeks"},{"type_text":u"月热量","nav_calories":True,"type":"Months"}],"type":"Cal","num":2},
    {"period":[{"type_text":u"日距离","nav_distance":True,"type":"Days"},{"type_text":u"周距离","nav_distance":True,"type":"Weeks"},{"type_text":u"月距离","nav_distance":True,"type":"Months"}],"type":"Dis","num":3},
    {"period":[{"type_text":u"日睡眠","nav_sleep":True,"type":"Days"},{"type_text":u"周睡眠","nav_sleep":True,"type":"Weeks"},{"type_text":u"月睡眠","nav_sleep":True,"type":"Months"}],"type":"Sleep","num":4},
    ]
    data["chart_data_day"] = [
                {
                    "date": "2015-11-29",
                    "step_object": 300,
                    "step_value": 508,
                    "cal_object": 2000,
                    "cal_value": 1500
                },
                {
                    "date": "2015-11-30",
                    "step_object": 482,
                    "step_value": 520,
                    "cal_object": 1000,
                    "cal_value": 500
                },
                {
                    "date": "2015-12-01",
                    "step_object": 430,
                    "step_value": 562,
                    "cal_object": 2000,
                    "cal_value": 3500
                },
                {
                    "date": "2015-12-02",
                    "step_object": 500,
                    "step_value": 379,
                    "cal_object": 2000,
                    "cal_value": 2500
                },
                {
                    "date": "2015-12-03",
                    "step_object": 700,
                    "step_value": 501,
                    "cal_object": 1800,
                    "cal_value": 2000
                },
                {
                    "date": "2015-12-04",
                    "step_object": 650,
                    "step_value": 443,
                    "cal_object": 2000,
                    "cal_value": 1500
                },
                {
                    "date": "2015-12-05",
                    "step_object": 200,
                    "step_value": 405,
                    "cal_object": 1000,
                    "cal_value": 1500
                },
                {
                    "date": "2015-12-06",
                    "Size": 14,
                    "step_object": 400,
                    "step_value": 309,
                    "cal_object": 2500,
                    "cal_value": 1000
                },
                {
                    "date": "2015-12-07",
                    "step_object": 500,
                    "step_value": 287,
                    "cal_object": 2000,
                    "cal_value": 3500
                },
                {
                    "date": "2015-12-08",
                    "step_object": 800,
                    "step_value": 485,
                    "cal_object": 3000,
                    "cal_value": 1000
                },
                {
                    "date": "2015-12-09",
                    "step_object": 500,
                    "step_value": 890,
                    "cal_object": 2000,
                    "cal_value": 1500
                },
                {
                    "date": "2015-12-10",
                    "step_object": 500,
                    "step_value": 810,
                    "cal_object": 2592,
                    "cal_value": 1222
                },
                {
                    "date": "2015-12-11",
                    "step_object": 800,
                    "step_value": 670,
                    "cal_object": 2050,
                    "cal_value": 2500
                },
                {
                    "date": "2015-12-12",
                    "step_object": 360,
                    "step_value": 540,
                    "cal_object": 2200,
                    "cal_value": 1760
                }
            ]
    data["chart_data_week"] = [
                {
                    "date": "2015-11-12",
                    "step_object": 1320,
                    "step_value": 1000,
                    "week": 46,
                    "cal_object": 22000,
                    "cal_value": 31500
                },
                {
                    "date": "2015-11-19",
                    "step_object": 820,
                    "step_value": 1882,
                    "week": 47,
                    "cal_object": 19000,
                    "cal_value": 18050              
                },
                {
                    "date": "2015-11-26",
                    "step_object": 3200,
                    "step_value": 4809,
                    "week": 48,
                    "cal_object": 19540,
                    "cal_value": 10101          
                },
                {
                    "date": "2015-12-05",
                    "step_object": 2820,
                    "step_value": 3000,
                    "week": 49,
                    "cal_object": 14000,
                    "cal_value": 16800
                },
                {
                    "date": "2015-12-12",
                    "step_object": 3000,
                    "step_value": 2500,
                    "week": 50,
                    "cal_object": 15000,
                    "cal_value": 17000
                },
                {
                    "date": "2015-12-19",
                    "step_object": 3000,
                    "step_value": 2500,
                    "week": 51,
                    "cal_object": 20500,
                    "cal_value": 15000
                },
                {
                    "date": "2015-12-25",
                    "step_object": 4000,
                    "step_value": 5500,
                    "week": 52,
                    "cal_object": 25012,
                    "cal_value": 23013
                },
                {
                    "date": "2016-01-02",
                    "step_object": 5000,
                    "step_value": 3000,
                    "week": 53,
                    "cal_object": 20040,
                    "cal_value": 17231
                }
            ]
    data["chart_data_month"] = [
                {
                    "date":"2015-06",
                    "step_object":12346,
                    "step_value":61234,
                    "cal_object":50231,
                    "cal_value":43212
                },
                {
                    "date":"2015-07",
                    "step_object":12347,
                    "step_value":71234,
                    "cal_object":55231,
                    "cal_value":62212
                },
                {
                    "date":"2015-08",
                    "step_object":12348,
                    "step_value":81234,
                    "cal_object":32142,
                    "cal_value":26515
                },
                {
                    "date":"2015-09",
                    "step_object":56700,
                    "step_value":79682,
                    "cal_object":61256,
                    "cal_value":43212
                },
                {
                    "date":"2015-10",
                    "step_object":70000,
                    "step_value":54000, 
                    "cal_object":34151,
                    "cal_value":33212

                },
                {
                    "date":"2015-11",
                    "step_object":36000,
                    "step_value":54000,
                    "cal_object":42231,
                    "cal_value":33212
                },
                {
                    "date":"2015-12",
                    "step_object":5600,
                    "step_value":2400,              
                    "cal_object":12231,
                    "cal_value":25612
                },
                {
                    "date":"2016-01",
                    "step_object":1230,
                    "step_value":5430,              
                    "cal_object":20231,
                    "cal_value":14612
                }
            ]
    if not flag:
        data["plans"] = []
        plans = user.user_plan_members.all()
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
        matchs = match_tools.getAllMatch(user)
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
    return HttpResponse(json.dumps(data), content_type="application/json")
    
def friend_add(request):
#    try:
        user = request.GET["userId"]
        user = User.objects.get(openId=user)
        id = int(request.GET["target"])
        type = int(request.GET["type"])
        if type == 0:
            target = User.objects.get(openId=id)
            user.friends.add(target)
        else:
            target = user.friend.filter(openId=id)
            user.friends.remove(target)
        return HttpResponse("success")
#    except:
#        return HttpResponse("error")