import datetime
from models import User, Data

class Object:
   def __init__(self):
       None

def date_splitter(datetime):
    d1,d2 = datetime.split(" ")
    d1 = d1.split("-")
    d2 = d2.split(":")
    for i in xrange(3):
        d1[i] = int(d1[i])
        d2[i] = int(d2[i])
    d0 = []
    for i in xrange(3):
        d0.append(d1[i])
    for i in xrange(3):
        d0.append(d2[i])
    return d0

def leq(dt1, dt2):
    flag = True
    for i in xrange(6):
        if dt1[i] < dt2[i]:
            return True
        else:
            flag = dt1[i] == dt2[i]
    return flag

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

def valid(s1, e1, s2, e2):
    rs1 = date_splitter(s1)
    re1 = date_splitter(e1)
    return leq(s2, rs1) and leq(re1, e2)

def Calories(d1, d2, user):
    result = 0
    data = User.objects.get(openId=user).basic_data.all()
    for item in data:
        if valid(item.startTime, item.endTime, d1, d2):
            result += item.calories
    result = int(result / 4.1858)
    return result    

def today_Calories(user):
    today = modifiedData()
    today[3] = today[4] = today[5] = 0
    tomorrow = today
    tomorrow[2] += 1
    if tomorrow[2] > monthDays(tomorrow[0], tomorrow[1]):
        tomorrow[2] = 1
        tomorrow[1] += 1
    if tomorrow[1] > 12:
        tomorrow[1] = 1
        tomorrow[0] += 1
    return Calories(today, tomorrow, user)

