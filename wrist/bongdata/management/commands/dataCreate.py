import random
from django.core.management.base import BaseCommand, CommandError
from bongdata.models import BongData
from basic.models import Data, User

def CreateData():
    origin_data = BongData.objects.all()
    users = User.objects.all()
    for user in users:
        for item in origin_data:
            tmp = user.basic_data.filter(startTime=item.startTime)
            if len(tmp) == 0:
                if random.random() < 0.5:
                    tmp_data = Data(user=user,startTime=item.startTime,endTime=item.endTime,type=item.type,
                               subType=item.subType,distance=item.distance,speed=item.speed,calories=item.calories,
                               steps=item.steps,actTime=item.actTime,nonActTime=item.nonActTime,dsNum=item.dsNum,
                               lsNum=item.lsNum,wakeNum=item.wakeNum,wakeTimes=item.wakeTimes,score=item.score)
                    tmp_data.save()
            else:
                if random.random() < 0.5:
                    tmp[0].endTime=item.endTime
                    tmp[0].type=item.type
                    tmp[0].subType=item.subType
                    tmp[0].distance=item.distance
                    tmp[0].speed=item.speed
                    tmp[0].calories=item.calories
                    tmp[0].steps=item.steps
                    tmp[0].actTime=item.actTime
                    tmp[0].nonActTime=item.nonActTime
                    tmp[0].dsNum=item.dsNum
                    tmp[0].lsNum=item.lsNum
                    tmp[0].wakeNum=item.wakeNum
                    tmp[0].wakeTimes=item.wakeTimes
                    tmp[0].score=item.score
                    tmp[0].save()
 
class Command(BaseCommand):
    def handle(self, *args, **options):
        CreateData()        
