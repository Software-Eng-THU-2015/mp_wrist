#-*- coding=utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from basic.models import User, Data, DayData
from basic import tools

class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            user.comment = u"本周的健康报告"
            user.save()
