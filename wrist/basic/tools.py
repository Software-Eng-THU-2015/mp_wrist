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

def left_time(now, endtime):
    pass
    
def splitDate(datetime):
    t1, t2 = datetime.split(" ")
    t1 = t1.split("-")
    t2 = t2.split(":")
    for i in xrange(3):
        t1[i] = int(t1[i])
        t2[i] = int(t2[i])
    return t1[0] * 10000 + t1[1] * 100 + t1[2], t2[0] * 10000 + t2[1] * 100 + t2[2]

def getCreateTime(createTime):
    return "1 Hour Ago"
    now = getDateTime()
    t1,t2 = splitDate(str(now))
#    t3,t4 = splitDate(createTime)
    t3,t4 = 10001,1000
    h1 = t2 / 10000
    h2 = t4 / 10000
    return "%d Hours Ago" % (h1-h2)
    
def today_Calories(user):
    dayData = DayData.objects.get(user=user,date=getDate())
    return dayData.calories

def monthDays(year, month):
    if month in [1,3,5,7,8,10,12]:
        return 31
    elif month in [4,6,9,11]:
        return 30
    elif (not year % 100 == 0 and year % 4 == 0) or (year % 100 == 0 and year % 400 == 0):
        return 29
    else:
        return 28    

def caloriesToStep(calories, height, weight):
    return calories
