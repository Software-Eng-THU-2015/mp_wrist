#-*- coding=utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from basic.models import User, Data, DayData
from basic import tools
from wechat import tools as wechat_tools

class Command(BaseCommand):
    def handle(self, *args, **options):
        date = tools.getDate()
        users = User.objects.all()
        for user in users:
            if DayData.objects.filter(user=user,date=date).count() > 0:
                dayData = DayData.objects.filter(user=user,date=date)[0]
                steps = dayData.steps
                steps_goal = dayData.steps_goal
                if steps >= steps_goal:
                    per = 100
                else:
                    per = int(steps * 100 / steps_goal)
                url = "%s/basic/redirect/profile?page=0"
                data = {
                  "steps":{
                   "value": str(dayData.steps),
                   "color": "#ff0000",
                   },
                   "per":{
                    "value": str(per),
                    "color": "#007fff"
                   },
                   "remark":{
                    "value": u"点击查看详细信息",
                    "color": "#666666"
                   }
                }
                wechat_tools.customSendTemplate(user.openId, wechat_tools.template_id["data"], "#000000", data, url)
