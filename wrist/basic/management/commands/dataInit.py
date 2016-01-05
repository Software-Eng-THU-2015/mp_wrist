#-*- coding=utf-8 -*-
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
            if DayData.objects.filter(user=user,date=date).count() == 0:
                dayData = DayData(user=user,date=date)
                tools.updateDayData(dayData, user)
                dayData.save()
            Data.objects.filter(user=user,date=preDate(date)).delete()
