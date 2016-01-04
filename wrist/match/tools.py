#-*- coding=utf-8 -*-

from basic.models import User, Team
from match.models import Match, MatchProgress
from wechat import tools as wechat_tools

def closest_match(user, now):
    match = user.user_match_members.order_by('endTime').filter(finished=0)
    if match.count() > 0:
        return match[0]
    else:
        return None
    
def findTeam(match, user):
    teams = match.members.all()
    userId = user.openId
    for team in teams:
        if team.members.filter(openId=userId).exists():
            return team
    return None
    
def getSingleProgress(match, user):
    progress = MatchProgress.objects.filter(match=match,user=user)
    if progress.count() == 0:
        return 0
    else:
        return progress[0].value
    
def getProgress(match, user):
    team = findTeam(match, user)
    members = team.members.all()
    result = 0
    for member in members:
        result += getSingleProgress(match, member)
    
def getDefaultImageByTag(tags):
    return "/static/img/match_make.jpg"
    
def sendInvite(user, id, friendId, type):
    url = "%s/match/redirect/profile?page=3&id=%d" % (wechat_tools.domain, id)
    match = Match.objects.get(id=id)
    if type == 0:
        identity = u"队友"
    else:
        identity = u"对手"
    data = {
      "friend":{
        "value": user.name,
        "color": "#ff0000",
      },
      "name":{
        "value": u"%s比赛" % match.name,
        "color": "#007fff",
      },
      "identity":{
        "value": identity,
        "color": "#ff0000",
      },
      "remark":{
        "value": u"详情请点击查看",
        "color": "#666666"
      }
    }
    wechat_tools.customSendTemplate(friendId, wechat_tools.template_id["invite"], "#000000", data, url)