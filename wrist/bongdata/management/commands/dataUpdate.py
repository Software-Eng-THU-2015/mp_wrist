import datetime
import requests
import shelve
from django.core.management.base import BaseCommand, CommandError
from bongdata.models import BongData

g_data = [
 "token_url": "http://open-test.bong.cn/oauth/token",
 "url": "http://open-test.bong.cn/1/bongday/blocks/",
 "file_url": "/data/www/wrist/bongdata.shelve",
 "user_num": 9,
 "file": None
]

def getToken(user, uid, client_id, client_sec):
    f = g_data["file"]
    refresh_token = f[user]["refresh_token"]
    res = requests.request(method="get", url="%s?client_id=%s&grant_type=refresh_token&client_secret=%s&refresh_token=%s" % (g_data["token_url"], client_id, client_sec, refresh_token))
    res.encoding = "utf-8"
    data = res.json()
    if "error" in data:
        return "error"
    f[user] = {"uid": uid, "access_token": data["access_token"], "refresh_token": data["refresh_token"]}  
    return data["access_token"]

def monthDays(year, month):
    if month in [1,3,5,7,8,10,12]:
        return 31
    elif month in [4,6,9,11]:
        return 30
    elif (not year % 100 == 0 and year % 4 == 0) or (year % 100 == 0 and year % 400 == 0):
        return 29
    else:
        return 28

def modifiedData():
    d1, d2 = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S").split(" ")
    d3 = d1.split("-")
    d4 = d2.split(":")
    for i in xrange(3):
        d3[i] = int(d3[i])
        d4[i] = int(d4[i])
    d4[0] += 8
    if d4[0] > 23:
        d4[0] -= 24
        d3[2] += 1
    if d3[2] > monthDays(d3[0], d3[1]):
        d3[2] = 1
        d3[1] += 1
    if d3[1] > 12:
        d3[1] = 1
        d3[0] += 1
    for i in xrange(3):
        d3.append(d4[i])
    return d3

def getData(user, uid, access_token, client_id, client_sec):
    tmp = modifiedData()
    date = "%04d%02d%02d" % (tmp[0], tmp[1], tmp[2])
    res = requests.request(method="get", url="%s%s?uid=%s&access_token=%s" % (url, date, uid, access_token))
    res.encoding = "utf-8"
    data = res.json()
    if "error" in data:
        access_token = getToken(user, uid, client_id, client_sec)
        if access_token == "error":
            return -1
        res = requests.request(method="get", url="%s%s?uid=%s&access_token=%s" % (url, date, uid, access_token))
        res.encoding = "utf-8"
        data = res.json()
    data = data["value"]
    for item in data:
        try:
            save_item = BongData.objects.get(startTime=item["startTime"])
        except:
            save_item = BongData(startTime=item["startTime"])
        save_item.user = int(user)
        save_item.userId = uid
        if "endTime" in item:
            save_item.endTime=item["endTime"]
        if "type" in item:
            save_item.type = int(item["type"])
        if "subType" in item:
            save_item.subType = int(item["subType"])
        if "distance" in item:
            save_item.distance = int(item["distance"])
        if "speed" in item:
            save_item.speed = int(item["speed"])
        if "calories" in item:
            save_item.calories = int(item["calories"])
        if "steps" in item:
            save_item.steps = int(item["steps"])
        if "actTime" in item:
            save_item.actTime = int(item["actTime"])
        if "nonActTime" in item:
            save_item.nonActTime = int(item["nonActTime"])
        if "dsNum" in item:
            save_item.dsNum = int(item["dsNum"])
        if "lsNum" in item:
            save_item.lsNum = int(item["lsNum"])
        if "wakeNum" in item:
            save_item.wakeNum = int(item["wakeNum"])
        if "wakeTimes" in item:
            save_item.wakeTimes = int(item["wakeTimes"])
        if "score" in item:
            save_item.score = int(item["score"])
        save_item.save()

class Command(BaseCommand):
    def handle(self, *args, **options):
        f = shelve.open(file_url)
        g_data["file"] = f
        client_id = f["client_id"]
        client_sec = f["client_sec"]
        for i in xrange(user_num):
            user = str(i)
            uid = f[user]["uid"]
            access_token = f[user]["access_token"]
            getData(user, uid, access_token, client_id, client_sec)
        f.close()
        print "hello world"
