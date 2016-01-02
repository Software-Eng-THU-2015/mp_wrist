import json
import httplib
from django.core.management.base import BaseCommand, CommandError
from basic.models import User, DayData, Data
from basic import tools

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
    dayData.calories = dayData.calories + data.calories
    dayData.steps = dayData.steps + data.steps
    dayData.sleep = dayData.sleep + data.lsNum + data.dsNum
    dayData.save()

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
