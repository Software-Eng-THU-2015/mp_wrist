#-*- coding=utf-8 -*-
###
# description: 微信公众号被动回复服务
###

__author__ = "chendaxixi"

import random
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from wechatpy import parse_message, create_reply
from wechatpy.replies import TextReply, ImageReply, VoiceReply, VideoReply, MusicReply, ArticlesReply, TransferCustomerServiceReply
from basic.models import User, DayData
from basic import tools as basic_tools
from match.models import Match
from match import tools as match_tools
from wechat import tools

@csrf_exempt
def handle(request):
    if request.method == "GET":
        if not tools.checkSignature(request):
            return HttpResponse("invalid signature")
        else:
            return HttpResponse(request.GET["echostr"]) 
    msg = parse_message(request.body)
    return msg_splitter[msg.type](msg)

#对文本信息进行回复
def textHandle(msg):
    #生成文本回复
    return HttpResponse(create_reply(tools.help_text, message=msg))

#对语音信息进行回复
def voiceHandle(msg):    
    return HttpResponse(create_reply(tools.help_text, message=msg))

#对图片信息进行回复
def imageHandle(msg):
    return HttpResponse(create_reply(tools.help_text, message=msg))

#对视频信息进行回复
def videoHandle(msg):
    return HttpResponse(create_reply(tools.help_text, message=msg))

#对地理位置信息进行回复
def locationHandle(msg):
    return HttpResponse(create_reply(tools.help_text, message=msg))

#对链接信息进行回复
def linkHandle(msg):
    return HttpResponse(create_reply(tools.help_text, message=msg))

#对小视频信息进行回复
def svHandle(msg):
    return HttpResponse(create_reply(tools.help_text, message=msg))

#对事件信息进行处理
def eventHandle(msg):
    return event_splitter[msg.event](msg)

#用户关注事件
def subEvent(msg):
    data = tools.client.user.get(msg.source)
    try:
        username = data["nickname"]
        users = User.objects.filter(openId=msg.source)
        if len(users) > 0:
            user = users[0]
        else:
            user = User(name=data["nickname"],sex=int(data["sex"]),openId=msg.source)
        user.name = username
        user.uid = int(random.random() * 100)
        if "headimgurl" in data:
            user.image = data["headimgurl"]
        user.save()
        date = basic_tools.getDate()
        #如果DayData不存在，则创建
        tmp = DayData.objects.filter(user=user,date=date)
        if len(tmp) == 0:
            dayData = DayData(user=user,date=date)
            dayData.save()
    except:
        username = ""
    return HttpResponse(create_reply(u"%s!欢迎使用新中韩无敌了的手环公众号!\n%s" % (username, tools.help_text), message=msg))

#对用户取消关注事件
def unsubEvent(msg):
#    try:
#        user = User.objects.get(openId=msg.source)
#        user.delete()
#    except:
#        user = None
    return HttpResponse(create_reply(u"Hello World!I am 用户取关事件", message=msg))

#未关注用户扫描带参数二维码事件
def subscanEvent(msg):
    return HttpResponse(create_reply(u"Hello World!I am 未关注用户扫描带参数二维码事件", message=msg))

#已关注用户扫描带参数二维码事件
def scanEvent(msg):
    return HttpResponse(create_reply(u"Hello World!I am 已关注用户扫描带参数二维码事件", message=msg))

#上报地理位置事件
def locationEvent(msg):
    return HttpResponse(create_reply(u"Hello World!I am 上报地理位置事件", message=msg))

#点击菜单拉取消息事件
def clickEvent(msg):
    reply = TextReply(content=u"I am 菜单拉取事件", message=msg)
    user = User.objects.get(openId=msg.source)
    id = user.id
    data = tools.client.user.get(msg.source)
    #更新用户姓名、头像
    user.name = data["nickname"]
    if "headimgurl" in data:
        user.image = data["headimgurl"]
    else:
        user.image = ""
    user.save()
    date = basic_tools.getDate()
    datetime = basic_tools.getDateTime()
    now = basic_tools.getNow()
    if msg.key == "V1001_DATA_TODAY": #今日战况
        data = DayData.objects.filter(user=user,date=date)
        if len(data) == 0:
            data = DayData(user=user,date=date)
            data.save()
        else:
            data = data[0]
        steps = data.steps
        dayPlan = user.dayPlan
        if steps < dayPlan:
           per = steps * 100 / dayPlan
        else:
           per = 100
        if per <= 25:
           remark = u"前路漫漫，要加油噢!"
        elif per >= 40 and per <= 60:
           remark = u"成功的路已经走了一半，继续努力!"
        elif per == 100:
           remark = u"已经完成预定计划了！你真棒！"
        elif per >= 90:
           remark = u"就快要成功了！加油加油!"
        else:
           remark = ""
        url = "%s/basic/redirect/profile?page=0" % tools.domain
        data = {
          "steps":{
            "value": str(steps),
            "color": "#ff0000",
          },
          "per":{
            "value": str(per),
            "color": "#007fff",
          },
          "remark":{
            "value": remark,
            "color": "#666666"
          }
        }
        tools.customSendTemplate(msg.source, tools.template_id["data"], "#000000", data, url)
        reply = ""
    elif msg.key == "V1001_DATA_BIND": #绑定手环
        url = "%s/basic/bind?openId=%s" % (tools.domain, msg.source)
        data = {
          "content":{
            "value": u"请点击进入绑定",
            "color": "#ff5656"
          }
        }
        tools.customSendTemplate(msg.source, tools.template_id["msg"], "#000000", data, url) 
        reply = ""
    elif msg.key == "V1001_DATA_HELP": #帮助
        reply = TextReply(content=tools.help_text, message=msg)
    elif msg.key == "V1001_DATA_PROFILE": #个人主页
        dayPlan = user.dayPlan
        sleepPlan = user.sleepPlan
        if dayPlan == 0 or sleepPlan == 0:
            remark = u"您的计划设置不完整，请点击进入设置"
        else:
            remark = user.comment
            if remark == "":
                remark = u"点击查看个人信息"
        url = "%s/basic/redirect/profile?page=3" % tools.domain
        data = {
            "dayPlan":{
              "value": str(dayPlan),
              "color": "#ff0000"
            },
            "sleepPlan":{
              "value": str(sleepPlan),
              "color": "#007fff"
            },
            "remark":{
              "value": remark,
              "color": "#666666"
            }
        }
        tools.customSendTemplate(msg.source, tools.template_id["profile"], "#000000", data, url)
        reply = ""
    elif msg.key == "V1001_PLAN_MAKE":  #制定计划
        articles = []
        articles.append({"title":u"制定计划","description":u"快来制定你自己的运动计划吧!","image":"%s/static/img/plan_make.jpg" % tools.domain,"url":"%s/plan/redirect?page=0" % tools.domain})
        reply = ArticlesReply(articles=articles, message=msg)
    elif msg.key == "V1001_PLAN_OWN":   #我的计划
        articles = []
        articles.append({"title":u"查看我的","description":u"来看看你都有什么运动计划吧","image":"%s/static/img/plan_own.jpg" % tools.domain,"url":"%s/plan/redirect?page=3" % tools.domain})
        reply = ArticlesReply(articles=articles, message=msg)
    elif msg.key == "V1001_PLAN_SQUARE":    #计划广场
        articles = []
        articles.append({"title":u"计划广场","description":u"新鲜出炉的运动计划","image":"%s/static/img/plan_square.jpg" % tools.domain,"url":"%s/plan/redirect?page=2" % tools.domain})
        reply = ArticlesReply(articles=articles, message=msg)
    elif msg.key == "V1001_PLAN_RANK":  #计划排行榜
        articles = []
        articles.append({"title":u"计划排行榜","description":u"想知道什么计划更受欢迎么","image":"%s/static/img/plan_rank.jpg" % tools.domain,"url":"%s/plan/redirect?page=1" % tools.domain})
        reply = ArticlesReply(articles=articles, message=msg)
    elif msg.key == "V1001_MATCH_MAKE": #创建比赛
        articles = []
        articles.append({"title":u"创建比赛","description":u"开始一场新的比赛吧！","image":"%s/static/img/match_make.jpg" % tools.domain,"url":"%s/match/redirect?page=0" % tools.domain})
        reply = ArticlesReply(articles=articles, message=msg)
    elif msg.key == "V1001_MATCH_CHECK":    #我的比赛进度查看
        closest_match = match_tools.closest_match(now)
        if not closest_match:   #没有未结束的比赛
            data = {
                "title":{
                    "value": u"比赛进度提醒",
                    "color": "#000000"
                },
                "content":{
                    "value": u"没有未结束的比赛",
                    "color": "#ff0000"
                },
                "remark":{
                    "value": u"来亲自发起一场比赛吧!",
                    "color": "#666666"
                }
            }
            url = "%s/match/redirect?page=0" % tools.domain
            tools.customSendTemplate(msg.source, tools.template_id["msg"], "#000000", data, url)
        else:   #返回最近的比赛的进度
            left_time = basic_tools.left_time(now, closest_match.endtime)
            steps = match_tools.steps_sum(closest_match)
            data = {
                "object":{
                    "value": u"%s 比赛" % closest_match.title,
                    "color": "#007fff"
                },
                "lastTime":{
                    "value": left_time,
                    "color": "#ff0000"
                },
                "steps":{
                    "value": str(steps),
                    "color": "#007fff"
                },
                "remark":{
                    "value": u"请继续努力!",
                    "color": "#666666"
                }
            }
            url = "%s/match/redirect?page=1" % tools.domain
            tools.customSendTemplate(msg.source, tools.template_id["progress"], "#000000", data, url)
        reply = ""
    elif msg.key == "V1001_MATCH_SQUARE": #比赛广场
        articles = []
        articles.append({"title":u"比赛广场","description":u"新鲜出炉的比赛","image":"%s/static/img/match_square.jpg" % tools.domain,"url":"%s/match/redirect?page=2" % tools.domain})
        reply = ArticlesReply(articles=articles, message=msg)
    return HttpResponse(reply)

#点击菜单跳转链接事件
def viewEvent(msg):
    return HttpResponse(create_reply(u"Hello World!I am 点击菜单跳转链接事件", message=msg))

#群发消息发送任务完成事件
def masssendEvent(msg):
    return HttpResponse(create_reply(u"Hello World!I am 群发消息发送任务完成事件", message=msg))

#模板消息发送任务完成事件
def templatesendEvent(msg):
    return HttpResponse(create_reply(u"Hello World!I am 模板消息发送任务完成事件", message=msg))

#扫码推事件
def sc_pushEvent(msg):
    return HttpResponse(create_reply(u"Hello World!I am 扫码推事件", message=msg))

#扫码推事件且弹出“消息接收中”提示框
def sc_waitEvent(msg):
    return HttpResponse(create_reply(u"Hello World!I am 扫码推事件且弹出“消息接收中”提示框", message=msg))

#弹出系统拍照发图事件
def pic_photo_Event(msg):
    return HttpResponse(create_reply(u"Hello World!I am 弹出系统拍照发图事件", message=msg))

#弹出拍照或者相册发图事件
def pic_photo_album_Event(msg):
    return HttpResponse(create_reply(u"Hello World!I am 弹出拍照或者相册发图事件", message=msg))

#弹出微信相册发图器事件
def pic_wechat_Event(msg):
    return HttpResponse(create_reply(u"Hello World!I am 弹出微信相册发图器事件", message=msg))

#弹出地理位置选择器事件
def select_location_Event(msg):
    return HttpResponse(create_reply(u"Hello World!I am 弹出地理位置选择器事件", message=msg))

msg_splitter = {
  "text": textHandle,
  "voice": voiceHandle,
  "image": imageHandle,
  "video": videoHandle,
  "location": locationHandle,
  "link": linkHandle,
  "shortvideo": svHandle,
  "event": eventHandle,
}

event_splitter = {
  "subscribe": subEvent,
  "unsubscribe": unsubEvent,
  "subscribe_scan": subscanEvent,
  "scan": scanEvent,
  "location": locationEvent,
  "click": clickEvent,
  "view": viewEvent,
  "masssendjobfinish": masssendEvent,
  "templatesendjobfinish": templatesendEvent,
  "scancode_push": sc_pushEvent,
  "scancode_waitmsg": sc_waitEvent,
  "pic_sysphoto": pic_photo_Event,
  "pic_photo_or_album": pic_photo_album_Event,
  "pic_weixin": pic_wechat_Event,
  "location_select": select_location_Event,
}
