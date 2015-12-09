import datetime
from django.core.management.base import BaseCommand, CommandError
import tools

class Command(BaseCommand):
    def handle(self, *args, **options):
        tmp = tools.strToList(datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S"))        
        tmp[3] += 8
        if tmp[3] > 23:
            tmp[3] -= 24
            tmp[2] += 1
        if tmp[2] > tools.monthDays(tmp[0], tmp[1]):
            tmp[2] = 1
            tmp[1] += 1
        if tmp[1] > 12:
            tmp[1] = 1
            tmp[0] += 1
        date = tmp[0] * 10000 + tmp[1] * 100 + tmp[2]
        for i in xrange(100):
            tools.CreateData(i, date)
