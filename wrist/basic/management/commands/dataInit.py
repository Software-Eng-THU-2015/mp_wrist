from django.core.management.base import BaseCommand, CommandError
from basic.models import User, Data, DayData
from basic import tools

def preDate(date):
    y = date / 10000
    m = date % 10000 / 100
    d = date % 100
    d -= 1
    if d < 1:
        m -= 1
        if m < 1:
            m = 12
            y -= 1
        d = tools.monthDays(y, m)
    return y * 10000 + m * 100 + d


class Command(BaseCommand):
    def handle(self, *args, **options):
        date = tools.getDate()
        users = User.objects.all()
        for user in users:
            tmp = DayData.objects.filter(user=user,date=date)
            if len(tmp) == 0:
                dayData = DayData(user=user,date=date)
                dayData.save()
            list = Data.objects.filter(user=user,date=preDate(date))
            for data in list:
                data.delete()
