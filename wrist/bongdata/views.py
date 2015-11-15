import json
from django.shortcuts import render
from django.http import HttpResponse
from models import BongData

# Create your views here.

def date_splitter(datetime):
    result = {}
    date,realtime = datetime.split(" ")
    result["year"], result["month"], result["day"] = date.split("-")
    result["hour"], result["minute"], result["second"] = realtime.split(":")
    for item in result:
        result[item] = int(result[item])
    return result

def leq(dt1, dt2):
    prop = ["year", "month", "day", "hour", "minute", "second"]
    flag = True
    for i in prop:
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

def data(request):
#    try:
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
        if not type == 0 and not subType == 0:
            data = BongData.objects.filter(type=type,subType=subType)
        elif not type == 0:
            data = BongData.objects.filter(type=type)
        else:
            data = BongData.objects.all()
        result = []
        for item in data:
            if valid(item.startTime, item.endTime, start, end):
                tmp = {}
                tmp["startTime"] = item.startTime
                tmp["endTime"] = item.endTime
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
#    except:
#        return HttpResponse("404")
