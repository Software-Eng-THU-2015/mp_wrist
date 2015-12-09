import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import BongData

# Create your views here.

def monthDays(year, month):
    if month in [1,3,5,7,8,10,12]:
        return 31
    elif month in [4,6,9,11]:
        return 30
    elif (not year % 100 == 0 and year % 4 == 0) or (year % 100 == 0 and year % 400 == 0):
        return 29
    else:
        return 28

def date_splitter(datetime):
    date,realtime = datetime.split(" ")
    d1 = date.split("-")
    d2 = realtime.split(":")
    for i in xrange(3):
        d1[i] = int(d1[i])
        d2[i] = int(d2[i])
        d1.append(d2[i])
    if d1[3] == 24:
        d1[3] = 0
        d1[2] += 1
    if d1[2] > monthDays(d1[0], d1[1]):
        d1[2] = 1
        d1[1] += 1
    if d1[1] > 12:
        d1[1] = 1
        d1[0] += 1
    return d1
   
def leq(dt1, dt2):
    flag = True
    for i in xrange(6):
        if dt1[i] < dt2[i]:
            return True
        elif not dt1[i] == dt2[i]:
            flag = False
    return flag

def valid(s0, e0, s1, e1):
    rs0 = date_splitter(s0)
    rs1 = date_splitter(s1)
    re0 = date_splitter(e0)
    re1 = date_splitter(e1)
    return leq(rs1, rs0) and leq(re0, re1)

def strToInt(s):
    d = date_splitter(s)
    return d[0] * 10000 + d[1] * 100 + d[2]

def bongdata(date, type, subType, user):
    if not type == 0 and not subType == 0:
        if user > -1:
            return BongData.objects.filter(date=date,type=type,subType=subType,user=user)
        else:
            return BongData.objects.filter(date=date,type=type,subType=subType)
    elif not type == 0:
        if user > -1:
            return BongData.objects.filter(date=date,type=type,user=user)
        else:
            return BongData.objects.filter(date=date,type=type)
    else:
        if user > -1:
            return BongData.objects.filter(date=date,user=user)
        else:
            return BongData.objects.filter(date=date)

def data(request):
    try:
        start = request.GET["startTime"]
        end = request.GET["endTime"]
        try:
            type = request.GET["type"]
        except:
            type = 0
        try:
            subType = request.GET["subType"]
        except:
            subType = 0
        try:
            user = request.GET["user"]
        except:
            user = -1
        d1 = strToInt(start)
        d2 = strToInt(end)
        result = []
        for date in xrange(d1, d2+1):
            data = bongdata(date, type, subType, user)
            for item in data:
                if valid(item.startTime, item.endTime, start, end):
                    tmp = {}
                    tmp["startTime"] = item.startTime
                    tmp["endTime"] = item.endTime
                    tmp["date"] = item.date
                    tmp["user"] = item.user
                    tmp["type"] = item.type
                    tmp["subType"] = item.subType
                    tmp["distance"] = item.distance
                    tmp["calories"] = item.calories
                    tmp["steps"] = item.steps
                    tmp["actTime"] = item.actTime
                    tmp["nonActTime"] = item.nonActTime
                    tmp["dsNum"] = item.dsNum
                    tmp["lsNum"] = item.lsNum
                    tmp["wakeNum"] = item.wakeNum
                    tmp["wakeTimes"] = item.wakeTimes
                    tmp["score"] = item.score   
                    result.append(tmp)
        return HttpResponse(json.dumps(result), content_type="application/json")    
    except:
        return HttpResponse("404")

@csrf_exempt
def upload(request):
    try:
        user = request.GET["user"]
        date = request.GET["date"]
        json_data = json.loads(request.body)
        BongData.objects.filter(date=int(date),user=int(user)).delete()
        for item in json_data:
            new_item = BongData(user=int(user),userId='',date=int(date),startTime=item["startTime"],endTime=item["endTime"],type=item["type"])
            if "subType" in item:
                new_item.subType = item["subType"]
            if "distance" in item:
                new_item.distance = item["distance"]
            if "speed" in item:
                new_item.speed = item["speed"]
            if "calories" in item:
                new_item.calories = item["calories"]
            if "steps" in item:
                new_item.steps = item["steps"]
            if "actTime" in item:
                new_item.actTime = item["actTime"] 
            if "nonActTime" in item:
                new_item.nonActTime = item["nonActTime"]
            if "dsNum" in item:
                new_item.dsNum = item["dsNum"]
            if "lsNum" in item:
                new_item.lsNum = item["lsNum"]
            if "wakeNum" in item:
                new_item.wakeNum = item["wakeNum"]
            if "wakeTimes" in item:
                new_item.wakeTimes = item["wakeTimes"]
            if "score" in item:
                new_item.score = item["score"]
            new_item.save()
        return HttpResponse("success")
    except:
        return HttpResponse("404")
