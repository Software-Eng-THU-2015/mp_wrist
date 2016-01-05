#-*- coding=utf-8 -*-
import json
import httplib
from django.core.management.base import BaseCommand, CommandError
from basic.models import User, DayData, Data
from plan.models import Plan, PlanProgress
from match.models import Match, MatchProgress
from basic import tools
from wechat import tools as wechat_tools

def ArchiveCheck(user, data):
    return
    
def LevelCheck(user, data):
    user.steps += tool.caloriesToStep(data.calories, user.height, user.weight)
    user.save()
    flag = False
    while user.steps > tools.levelGap[user.level]:
        user.level += 1
        flag = True
    if flag:
        url = "%s/basic/redirect/profile?page=3"
        data = {
          "level":{
            "value":str(user.level),
            "color":"#ff0000",
          }
        }
        wechat_tools.customSendTemplate(user.openId, wechat_tools.template_id["levelUp"], "#000000", data, url)

def PlanCheck(user, plan, progress, oldValue):
    now = tools.getNow()
    url = "%s/plan/redirect/profile?page=4&id=%d" % (wechat_tools.domain, plan.id)
    if now > plan.endTime:
        plan.finished = 1
        plan.save()
        if plan.goal > 0 and progress.value >= plan.goal:
            content = u"恭喜您完成了计划"
        elif plan.goal > 0:
            content = u"很遗憾您没能完成计划"
        else:
            content = u"不知道您完成得怎么样呢"
        data = {
          "title":{
           "value": u"计划截止",
           "color": "#ff0000"
          },
          "content":{
           "value": u"%s计划已经截止,%s" % (plan.name, content),
           "color": "#007fff"
          },
          "remark": {
           "value": u"点击查看计划详情",
           "color": "#666666"
          }
        }
        wechat_tools.customSendTemplate(user.openId, wechat_tools.template_id["msg"], "#000000", data, url)
        return
    old_per = per = 0
    if plan.goal > 0:
        per = int(progress.value * 100 / plan.goal)
        old_per = int(oldValue * 100 / plan.goal)
    if per > 100:
        per = 100
    if per == 100:
        plan.finished = 1
        plan.save()
        data = {
          "title":{
           "value": u"计划完成",
           "color": "#ff0000"
          },
          "content":{
           "value": u"恭喜您提前完成了%s计划已经完成" % plan.name,
           "color": "#007fff"
          },
          "remark": {
           "value": u"点击查看计划详情",
           "color": "#666666"
          }
        }
        wechat_tools.customSendTemplate(user.openId, wechat_tools.template_id["msg"], "#000000", data, url)
    elif plan.endTime - now < 7200:
        if per < 90:
            remark = u"请抓紧时间!"
        else:
            remark = u"别错过了ddl噢"
        data = {
          "object":{
           "value": u"%s计划" % plan.name,
           "color": "#007fff"
          },
          "lastTime":{
           "value": tools.left_time(now, plan.endTime),
           "color": "#ff0000"
          },
          "steps":{
            "value": str(progress.value),
            "color": "#007fff"
          },
          "content":{
            "value": u"您已完成了%d\%" % per,
            "color": "#ff0000"
          },
          "remark": {
           "value": remark,
           "color": "#666666"
          }
        }
        wechat_tools.customSendTemplate(user.openId, wechat_tools.template_id["progress"], "#000000", data, url)
    elif (per > 80 and old_per < 80) or (per > 50 and old_per < 50) or (per > 20 and old_per < 20):
        if per > 80:
            remark = u"请继续努力"
        elif per > 50:
            remark = u"长路漫漫，还有一半"
        else:
            remark = u"好的开始是成功的一半"
        data = {
          "object":{
           "value": u"%s计划" % plan.name,
           "color": "#007fff"
          },
          "lastTime":{
           "value": tools.left_time(now, plan.endTime),
           "color": "#ff0000"
          },
          "steps":{
            "value": str(progress.value),
            "color": "#007fff"
          },
          "content":{
            "value": u"您已完成了%d\%" % per,
            "color": "#ff0000"
          },
          "remark": {
           "value": remark,
           "color": "#666666"
          }
        }
        wechat_tools.customSendTemplate(user.openId, wechat_tools.template_id["progress"], "#000000", data, url)

def PlansCheck(user, data):
    plans = user.user_plan_members.filter(finished=0)
    for plan in plans:
        progress = PlanProgress(plan=plan,user=user)
        oldValue = progress.value
        progress.value += tools.caloriesToStep(data.calories, user.height, user.weight)
        progress.save()
        PlanCheck(user, plan, progress, oldValue)
        
def MatchCheck(user, match, progress):
    now = tools.getNow()
    url = "%s/match/redirect/profile?page=3&id=%d" % (wechat_tools.domain, match.id)
    if now > match.endTime:
        match.finished = 1
        match.save()
        data = {
          "title":{
           "value": u"比赛结束",
           "color": "#ff0000"
          },
          "content":{
           "value": u"%s比赛已经截止,快来看看你们的战况吧!" % match.name,
           "color": "#007fff"
          },
          "remark": {
           "value": u"点击查看比赛详情",
           "color": "#666666"
          }
        }
        wechat_tools.customSendTemplate(user.openId, wechat_tools.template_id["msg"], "#000000", data, url)
    elif match.endTime - now < 7200:
        data = {
          "object":{
           "value": u"%s比赛" % match.name,
           "color": "#007fff"
          },
          "lastTime":{
           "value": tools.left_time(now, match.endTime),
           "color": "#ff0000"
          },
          "steps":{
            "value": str(progress.value),
            "color": "#007fff"
          },
          "remark": {
           "value": u"点击查看比赛详情",
           "color": "#666666"
          }
        }
        wechat_tools.customSendTemplate(user.openId, wechat_tools.template_id["progress"], "#000000", data, url)
 
def MatchsCheck(user, data):
    matchs = user.user_match_members.filter(finished=0)
    for match in matchs:
        progress = MatchProgress(match=match,user=user)
        progress.value += tools.caloriesToStep(data.calories, user.height, user.weight)
        progress.save()
        MatchCheck(user, match, progress)

def getData(uid, date):
    conn = httplib.HTTPConnection("wrist.ssast2015.com")
    conn.request("GET", "/bongdata/?user=%d&date=%d" % (uid, date))
    res = conn.getresponse()
    data = res.read()
    conn.close()
    data = json.loads(data)
    return data

def contains(user, data):
    tmp = Data.objects.filter(user=user,bongdata_id=data["id"])
    return len(tmp) > 0

def dataUpdate(data):
    try:
        dayData = DayData.objects.get(user=data.user, date=data.date)
    except:
        dayData = DayData(user=data.user,date=data.date)
        tools.updateDayData(dayData, data.user)
    dayData.calories = dayData.calories + data.calories
    tools.modifiedDayData(dayData, data.user)
    dayData.sleep = dayData.sleep + data.lsNum + data.dsNum
    dayData.save()
    PlansCheck(data.user, data)
    MatchsCheck(data.user, data)
    LevelCheck(data.user, data)
    ArchiveCheck(data.user, data)

class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()
        date = tools.getDate()
        for user in users:
            data_list = getData(int(user.uid), date)
            for data in data_list:
                if not contains(user, data):
                    new_data = Data(user=user,date=date,bongdata_id=data["id"],startTime=data["startTime"],
                      endTime=data["endTime"],type=data["type"],subType=data["subType"],distance=data["distance"],
                      calories=data["calories"],steps=data["steps"],actTime=data["actTime"],
                      nonActTime=data["nonActTime"],dsNum=data["dsNum"],lsNum=data["lsNum"],wakeNum=data["wakeNum"],
                      wakeTimes=data["wakeTimes"],score=data["score"])
                    new_data.save()
                    dataUpdate(new_data)
