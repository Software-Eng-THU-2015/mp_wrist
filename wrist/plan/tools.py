#-*- coding=utf-8 -*-

from basic.models import User
from plan.models import Plan, PlanProgress
from wechat import tools as wechat_tools

def getProgress(plan, user):
    progress = PlanProgress.objects.filter(plan=plan,user=user)
    if progress.count() == 0:
        return 0
    else:
        return progress[0].value

def getDefaultImageByTag(tags):
    return "/static/img/plan_make.jpg"
    
def sendInvite(user, id, friendId):
    url = "%s/plan/redirect/profile?page=4&id=%d" % (wechat_tools.domain, id)
    plan = Plan.objects.get(id=id)
    data = {
      "friend":{
        "value": user.name,
        "color": "#ff0000",
      },
      "name":{
        "value": u"%s计划" % plan.name,
        "color": "#007fff",
      },
      "identity":{
        "value": u"伙伴",
        "color": "#ff0000",
      },
      "remark":{
        "value": u"详情请点击查看",
        "color": "#666666"
      }
    }
    wechat_tools.customSendTemplate(friendId, wechat_tools.template_id["invite"], "#000000", data, url)