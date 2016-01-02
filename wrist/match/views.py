#-*- coding:utf-8 -*-

import random
import json
import time
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from basic.models import User, Good, Team
from basic import tools as basic_tools
from wechat import tools as wechat_tools
from models import Match, MTag

# Create your views here.

def redirect_match(request):
    if not "userId" in request.session:
        return HttpResponseRedirect("/static/not_bind.html")
    page = int(request.GET["page"])
    userId = request.session["userId"]
    if page == 0:
        url = "make"
    elif page == 1:
        url = "check"
    elif page == 2:
        url = "square"
    url = "/static/match/match_%s.html?%s" % (url, userId)
    return HttpResponseRedirect(url)

def match_make(request):
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if not request.GET["userId"] == request.session["userId"]:
        data = {"error":{"title":u"用户异常","content":u"请在公众号中创建自己的比赛"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    data = {}
    userId = data["userId"] = request.GET["userId"]
    user = User.objects.get(openId=userId)
    data["href"] = "%s/match/redirect" % wechat_tools.domain
    data["tags"] = []
    tags = MTag.objects.all()
    for tag in tags:
        data["tags"].append(tag.name)
    data["friends"] = []
    data["opponents"] = []
    friends = user.friends.all()
    for friend in friends:
        item = {}
        item["name"] = friend.name
        item["image"] = friend.image
        data["friends"].append(item)
        data["opponents"].append(item)
    return HttpResponse(json.dumps(data), content_type="application/json")
    
@csrf_exempt
def submit_make(request):
    userId = request.POST["userId"]
    user = User.objects.get(openId=userId)
    now = int(time.time())
    match = Match(title=request.POST["match_name"],description=request.POST["comment"],createTime=now,startTime="%s:00" % request.POST["begintime"],endTime="%s:00" % request.POST["endtime"],creator=user)
    match.endDate, match.endDateTime = basic_tools.splitDate(match.endTime)
    prefix = "/data/www/wrist"
    path = "/media/match/"
    if not os.path.exists(prefix+path):
        os.mkdir(prefix+path)
    file = request.FILES["image"]
    file_name = "%s%s_%s_%s" % (path, match.title.encode("utf-8"), str(now), file.name.encode("utf-8"))
    des = open(prefix+file_name, "wb")
    for chunk in file.chunks():
        des.write(chunk)
    des.close()
    match.image = file_name
    match.save()
    tags = request.POST["tags"].split("|")
    for tag in tags:
        item = MTag.objects.filter(name=tag)
        if len(item) == 0:
            item = MTag(name=tag)
            item.save()
        else:
            item = item[0]
        item.matchs.add(match)
    return HttpResponseRedirect("/match/redirect?page=3")

def match_square(request):
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    data = {}
    userId = data["userId"] = request.session["userId"]
    user = User.objects.get(openId=userId)
    data["href"] = "%s/match/redirect" % wechat_tools.domain
    data["data_list"] = []
    teams = Team.objects.all()
    data["teams"] = []
    for team in teams:
        item = {}
        item["name"] = team.name
        item["members"] = []
        members = team.members.all()
        for member in members:
            item["members"].append({"image":member.image,"name":member.name})
        data["teams"].append(item)
    matchs = Match.objects.all()[:20]
    for match in matchs:
        item = {}
        item["user_image"] = match.creator.image
        item["user_name"] = match.creator.name
        item["userId"] = match.id
        item["createTime"] = basic_tools.getCreateTime(match.createTime)
        item["title"] = match.title
        item["description"] = match.description
        item["image"] = match.image
        item["tags"] = []
        tags = match.match_mtag_matchs.all()
        for tag in tags:
            item["tags"].append(tag.name)
        teams = match.members.all()
        for team in teams:
            tmp = team.members.filter(openId=userId)
            if len(tmp) > 0:
                item["isFollow"] = 1
                break
        data["data_list"].append(item)
    data["data_list"].reverse()
    return HttpResponse(json.dumps(data), content_type="application/json")
    
def match_check(request):
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    data = {}
    userId = data["userId"] = request.session["userId"]
    user = User.objects.get(openId=userId)
    data["href"] = "%s/match/redirect" % wechat_tools.domain
    data["data_list"] = []
    matchs = user.user_match_creator.all()
    for match in matchs:
        item = {}
        item["user_image"] = match.creator.image
        item["user_name"] = match.creator.name
        item["createTime"] = basic_tools.getCreateTime(match.createTime)
        item["title"] = match.title
        item["description"] = match.description
        item["image"] = match.image
        item["tags"] = []
        tags = match.match_mtag_matchs.all()
        for tag in tags:
            item["tags"].append(tag.name)
        teams = match.members.all()
        for team in teams:
            tmp = team.members.filter(openId=userId)
            if len(tmp) > 0:
                item["isFollow"] = 1
                break
        data["data_list"].append(item)
    data["data_list"].reverse()
    return HttpResponse(json.dumps(data), content_type="application/json")
