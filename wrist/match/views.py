#-*- coding:utf-8 -*-

import random
import json
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
    elif page == 3:
        url = "profile"
        id = request.GET["id"]
        userId = "%s&%s" % (id, userId)
    url = "/static/match/match_%s.html?%s" % (url, userId)
    return HttpResponseRedirect(url)

def match_make(request):
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if not "userId" in request.GET:
        data = {"error":{"title":u"出错啦","content":u"这个页面找不到啦!"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if not request.GET["userId"] == request.session["userId"]:
        data = {"error":{"title":u"用户异常","content":u"请在公众号中创建自己的比赛"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    data = {}
    userId = data["userId"] = request.session["userId"]
    user = User.objects.get(openId=userId)
    data["href"] = "%s/match/redirect/profile" % wechat_tools.domain
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
    now = basic_tools.getNow()
    match = Match(title=request.POST["match_name"],description=request.POST["comment"],createTime=now,startTime=basic_tools.DateToInt("%s:00:00" % request.POST["begintime"][:13]),endTime=basic_tools.DateToInt("%s:00:00" % request.POST["endtime"][:13]),creator=user)
    prefix = os.environ.get("WRIST_HOME")
    path = "/media/match/"
    if not os.path.exists(prefix+path):
        os.mkdir(prefix+path)
    if "images" in request.FILES:
        file = request.FILES["image"]
        file_name = "%s%s_%s_%s" % (path, match.title.encode("utf-8"), str(now), file.name.encode("utf-8"))
        des = open(prefix+file_name, "wb")
        for chunk in file.chunks():
            des.write(chunk)
        des.close()
    else:
        file_name = "/static/img/plan_make.jpg"
    match.image = file_name
    match.save()
    tag = request.POST["tags"]
    if not tag == "":
        item = MTag.objects.filter(name=tag)
        if len(item) == 0:
            item = MTag(name=tag)
            item.save()
        else:
            item = item[0]
        item.matchs.add(match)
    i = 0
    while ("tag%d" % i) in request.POST:
        tag = request.POST["tag%d" % i]
        i += 1
        if not tag == "":
            item = MTag.objects.filter(name=tag)
            if len(item) == 0:
                item = MTag(name=tag)
                item.save()
            else:
                item = item[0]
            item.matchs.add(match)
    match.user_members.add(user)
    team = user.user_team_members.get(type=0)
    match.members.add(team)
    return HttpResponseRedirect("/match/redirect/profile?page=3&id=%d" % match.id)

def match_square(request):
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if not "userId" in request.GET:
        data = {"error":{"title":u"出错啦","content":u"这个页面找不到啦!"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    data = {}
    userId = data["userId"] = request.session["userId"]
    user = User.objects.get(openId=userId)
    data["href"] = "%s/match/redirect/profile" % wechat_tools.domain
    data["data_list"] = []
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
        if match.finished == 1:
            item["isFinished"] = 1
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
    if not "userId" in request.GET:
        data = {"error":{"title":u"出错啦","content":u"这个页面找不到啦!"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    data = {}
    userId = data["userId"] = request.session["userId"]
    user = User.objects.get(openId=userId)
    data["href"] = "%s/match/redirect/profile" % wechat_tools.domain
    data["data_list"] = []
    teams = Team.objects.all()
    matchs = user.user_match_members.all()[:20]
    for match in matchs:
        item = {}
        item["user_image"] = match.creator.image
        item["user_name"] = match.creator.name
        item["userId"] = match.id
        item["createTime"] = basic_tools.getCreateTime(match.createTime)
        item["title"] = match.title
        item["description"] = match.description
        item["image"] = match.image
        if match.finished == 1:
            item["isFinished"] = 1
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

def match_profile(request):
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if not "userId" in request.GET:
        data = {"error":{"title":u"出错啦","content":u"这个页面找不到啦!"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    data = {}
    userId = data["userId"] = request.session["userId"]
    user = User.objects.get(openId=userId)
    data["href"] = "%s/match/redirect/profile" % wechat_tools.domain
    data["data_list"] = []
    id = request.GET["id"]
    match = Match.objects.get(id=id)
    data["user_image"] = match.creator.image
    data["user_name"] = match.creator.name
    data["userId"] = match.id
    data["createTime"] = basic_tools.getCreateTime(match.createTime)
    data["title"] = match.title
    data["description"] = match.description
    data["image"] = match.image
    if match.finished == 1:
        data["isFinished"] = 1
    data["tags"] = []
    tags = match.match_mtag_matchs.all()
    for tag in tags:
        data["tags"].append(tag.name)
    tmp = match.user_members.filter(openId=userId)
    if len(tmp) > 0:
        data["isFollow"] = 1
    return HttpResponse(json.dumps(data), content_type="application/json")
    
def match_join(request):
    if not "userId" in request.session:
        return HttpResponse("error")
    if not "userId" in request.GET:
        return HttpResponse("error")
    matchId = int(request.GET["target"])
    match = Match.objects.get(id=matchId)
    userId = request.GET["userId"]
    user = User.objects.get(openId=userId)
    if not "team" in request.GET:
        team = tools.findTeam(match, user)
        match.user_members.remove(user)
        if team.type == 0:
            match.members.remove(team)
        else:
            team.members.remove(user)
        if len(match.user_members.all()) == 0:
            match.delete()
    else:
        teamId = int(request.GET["team"])
        if teamId == -1:
            team = user.user_team_members.get(type=0)
            match.members.add(team)
        else:
            team = Team.objects.get(id=teamId)
            if team.type == 0:
                member = team.members.all()[0]
                team = Team(name=basic_tools.teamName(team,user),type=1)
                team.members.add(member)
            team.members.add(user)
    return HttpResponse("success")
        
def match_list(request):
    if not "userId" in request.session:
        data = {"error":{"title":u"未绑定","content":u"请先到公众号绑定手环"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if not "userId" in request.GET:
        data = {"error":{"title":u"出错啦","content":u"这个页面找不到啦!"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if not request.GET["userId"] == request.session["userId"]:
        data = {"error":{"title":u"权限问题","content":u"这个页面找不到啦!"}}
        return HttpResponse(json.dumps(data), content_type="application/json")
    id = int(request.GET["target"])
    match = Match.objects.get(id=id)
    data = {"team":[]}
    teams = match.members.all()
    for team in teams:
        item = {}
        item["name"] = team.name
        item["id"] = team.id
        item["members"] = []
        members = team.members.all()
        for member in members:
            item["members"].append({"name":member.name,"image":member.image})
        data["team"].append(item)
    return HttpResponse(json.dumps(data), content_type="application/json")