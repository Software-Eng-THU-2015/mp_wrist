import random
from bongdata.models import BongData

def strToList(s):
    d1, d2 = s.split(" ")
    d3 = d1.split("-")
    d4 = d2.split(":")
    for i in xrange(3):
        d3[i] = int(d3[i])
        d4[i] = int(d4[i])
        d3.append(d4[i])
    return d3

def monthDays(year, month):
    if month in [1,3,5,7,8,10,12]:
        return 31
    elif month in [4,6,9,11]:
        return 30
    elif (not year % 100 == 0 and year % 4 == 0) or (year % 100 == 0 and year % 400 == 0):
        return 29
    else:
        return 28

def intToDate(date, time):
    year = date / 10000
    month = date % 10000 / 100
    day = date % 100
    hour = time / 10000
    minute = time % 10000 / 100
    second = time % 100
    if hour > 23:
        hour -= 24
        day += 1
    if day > monthDays(year, month):
        day = 1
        month += 1
    if month > 12:
        month = 1
        year += 1    
    return "%04d-%02d-%02d %02d:%02d:%02d" % (year, month, day, hour, minute, second)

def CreateActivity(user, date, startTime):
    item = BongData(startTime=intToDate(date, startTime),user=user,date=date,userId="")
    last = 0
    if (startTime <= 80000) or (startTime >= 110000 and startTime <= 150000 and random.random() < 0.25) or (startTime >= 230000 and random.random() < 0.8):
        item.type = 1
        item.subType = random.randint(1,3)
        subType = random.randint(1,3)
        item.subType = subType
        if subType == 1:
            last = random.randint(10, 180)
            item.dsNum = last
            item.score = last / 30 + 2
        elif subType == 2:
            last = random.randint(10, 300)
            item.lsNum = last
            item.score = last / 100 + 1
        elif subType == 3:
            last = random.randint(1, 30)
            item.wakeNum = last
            item.wakeTimes = random.randint(1, 5)
            item.score = (30-last) / 15
    elif random.random() < 0.1:
        item.type = 5
        last = random.randint(60, 120)
    elif random.random() < 0.25:
        item.type = 2
        subType = random.randint(1,6)
        item.subType = subType
        if subType == 1:
            last = random.randint(1,60)
            item.calories = int((random.random() * 0.2 + 0.9) * last)
            if random.random() < 0.6:
                item.distance = int(last * 60 * (random.random() * 0.2 + 0.9))
                item.steps = int(last * 60 * (random.random() * 0.2 + 0.9))
        elif subType == 2:
            last = random.randint(1,15)
            item.calories = random.randint(25,35) * last + random.randint(0,5)
            item.distance = int(last * 60 * (random.random() + 2.5))
            item.steps = int(item.distance / 0.9 + random.randint(0,30))
        elif subType == 3:
            last = random.randint(10,30)
            item.calories = random.randint(25,35) * last + random.randint(0,5)
            item.distance = int(last * 60 * (random.random() * 1.5 + 1.5))
        elif subType == 4:
            last = random.randint(10,30)
            item.calories = random.randint(35,45) * last + random.randint(0,3)
            item.distance = int(last * 60 * (random.random() * 5 + 5))
            item.steps = int(item.distance / 1.1 + random.randint(0,30))
        elif subType == 5:
            last = random.randint(10,30)
            item.calories = random.randint(15,25) * last + random.randint(0,10)
            item.distance = int(last * 60 * (random.random() + 0.5))
        else:
            last = random.randint(10,30)
            item.calories = random.randint(10,20) * last + random.randint(0,5)
            item.distance = int(last * 60 * (random.random() * 20 + 5))
    else:
        item.type = 3
        subType = random.randint(1,4)
        item.subType = subType
        if subType == 1:
            actTime = random.randint(0,180)
            nonActTime = random.randint(20 * actTime, 5 * 3600)
        elif subType == 2:
            actTime = random.randint(0, 2 * 3600)
            nonActTime = random.randint(0, actTime / 10)
        elif subType == 3:
            actTime = random.randint(0,180)
            nonActTime = random.randint(10 * actTime, 3600)
        else:
            actTime = random.randint(0,300)
            nonActTime = random.randint(0,120)
        last = (actTime + nonActTime) / 60
        item.calories = actTime / random.randint(6,12) + random.randint(0,5)
        if random.random() < 0.4:
            item.distance = int(item.calories * (random.random() * 6 + 2))
        item.actTime = actTime
        item.nonActTime = nonActTime
    hour = last / 60
    minute = last % 60
    if startTime % 10000 / 100 + minute >= 60:
        startTime += (hour + 1) * 10000 + (minute - 60) * 100
    else:
        startTime += hour * 10000 + minute * 100
    item.endTime = intToDate(date, startTime)
    item.save()
    return startTime         

def CreateData(user, date):
    item = BongData.objects.filter(user=user,date=date-1)
    ld = len(item)
    if ld == 0:
        startTime = 0
    else:
        tmp = strToList(item[ld-1].endTime)
        if tmp[0] * 10000 + tmp[1] * 100 + tmp[2] == date:
            startTime = tmp[3] * 10000 + tmp[4] * 100 + tmp[5]
        else:
            startTime = 0
    while startTime < 240000:
        startTime = CreateActivity(user, date, startTime)
