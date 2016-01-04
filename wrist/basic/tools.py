#-*- coding=utf-8 -*-

import time
import json
from models import User, DayData

bong_activity = [
  [u"睡眠", u"深睡眠", u"浅睡眠", u"清醒"],
  [u"剧烈运动", u"热身运动", u"健走", u"球类等运动", u"跑步", u"游泳", u"自行车"],
  [u"休闲运动", u"静坐", u"散步", u"交通工具", u"活动"],
  [u"摘下手环"],
  [u"手环充电"],
  [u"手环异常"]
]

def monthDays(year, month):
    if month in [1,3,5,7,8,10,12]:
        return 31
    elif month in [4,6,9,11]:
        return 30
    elif (not year % 100 == 0 and year % 4 == 0) or (year % 100 == 0 and year % 400 == 0):
        return 29
    else:
        return 28    

def getDate():
    date = time.strftime("%Y-%m-%d").split("-")
    for i in xrange(3):
        date[i] = int(date[i])
    return date[0] * 10000 + date[1] * 100 + date[2]

def getDateTime():
    date = time.strftime("%H:%M:%S").split(":")
    for i in xrange(3):
        date[i] = int(date[i])
    return date[0] * 10000 + date[1] * 100 + date[2]
    
def getNow():
    return int(time.time())
    
def getPreDate(date):
    y = date / 10000
    m = date % 10000 / 100
    d = date % 100
    d -= 1
    if d < 0:
        m -= 1
        if m < 1:
            m = 12
            y -= 1
        d = monthDays(y,m)
    return y * 10000 + m * 100 + d

def IntToDate(date):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(date))
  
def DateToInt(date):
    timeA = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(timeA))
    
def left_time(now, endtime):
    left = endtime - now
    sec = left % 60
    min = left % 3600 / 60
    hour = left % 86400 / 3600
    day = left / 86400
    if day > 0:
        return u"%d天%d小时%d分%d秒" % (day, hour, min, sec)
    elif hour > 0:
        return u"%d小时%d分%d秒" % (hour, min, sec)
    elif min > 0:
        return u"%d分%d秒" % (min, sec)
    else:
        return u"%d秒" % sec

def getCreateTime(createTime):
    now = getNow()
    left = now - createTime
    sec = left % 60
    min = left % 3600 / 60
    hour = left % 86400 / 3600
    day = left / 86400
    if day > 0:
        return u"%d 天前" % day
    elif hour > 0:
        return u"%d 小时前" % hour
    elif min > 0:
        return u"%d 分前" % min
    else:
        return u"%d 秒前" % sec

def caloriesToStep(calories, height, weight):
    return calories

def stepToCalories(steps, height, weight):
    return steps
    
def caloriesToDis(calories, height, weight):
    return calories
  
def stepToDis(steps, height, weight):
    return steps
    
def updateDayData(dayData, user):
    s = user.dayPlan
    h = user.height
    w = user.weight
    dayData.steps_goal = s
    dayData.calories_goal = stepToCalories(s,h,w)
    dayData.distance_goal = stepToDis(s,h,w)
    dayData.sleep_goal = user.sleepPlan

def modifiedDayData(dayData, user):
    c = dayData.calories
    h = user.height
    w = user.weight
    dayData.distance = caloriesToDis(c,h,w)
    dayData.steps = caloriesToStep(c,h,w)
    
def teamName(team, username):
    if not team:
        return username
    else:
        return u"%s的小队" % team.members.all()[0].name
