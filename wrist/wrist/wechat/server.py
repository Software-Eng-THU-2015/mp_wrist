
#-*- coding=utf-8 -*-
###
# description: 微信公众号被动回复服务
###

__author__ = "chendaxixi"

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from wechat import tools
from wechatpy import parse_message, create_reply
from wechatpy.replies import TextReply, ImageReply, VoiceReply, VideoReply, MusicReply, ArticlesReply, TransferCustomerServiceReply
from basic.models import User
from basic import tools as basic_tools

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
    reply = TextReply(content=u"你以为发文本有用么？太天真了!", message=msg)
    return HttpResponse(reply)

#对语音信息进行回复
def voiceHandle(msg):    
    return HttpResponse(create_reply("Hello World!I am voice", message=msg))

#对图片信息进行回复
def imageHandle(msg):
    return HttpResponse(create_reply("Hello World!I am image", message=msg))

#对视频信息进行回复
def videoHandle(msg):
    return HttpResponse(create_reply("Hello World!I am video", message=msg))

#对地理位置信息进行回复
def locationHandle(msg):
    return HttpResponse(create_reply("Hello World!I am location", message=msg))

#对链接信息进行回复
def linkHandle(msg):
    return HttpResponse(create_reply("Hello World!I am link", message=msg))

#对小视频信息进行回复
def svHandle(msg):
    return HttpResponse(create_reply("Hello World!I am short video", message=msg))

#对事件信息进行处理
def eventHandle(msg):
    return event_splitter[msg.event](msg)

#用户关注事件
def subEvent(msg):
    data = tools.client.user.get(msg.source)
    try:
        username = data["nickname"]
        try:
            user = User.objects.get(openId=msg.source)
        except:
            user = User(name=data["nickname"],sex=int(data["sex"]),openId=msg.source,goods=0)
        user.name = username
        if "headimgurl" in data:
            user.image = data["headimgurl"]
        user.save()
    except:
        username = ""
    return HttpResponse(create_reply(u"%s!欢迎使用新中韩无敌了的手环公众号!" % username, message=msg))

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
    user.name = data["nickname"]
    if "headimgurl" in data:
        user.image = data["headimgurl"]
    else:
        user.image = ""
    user.save()
    if msg.key == "V1001_DATA_TODAY": #今日战况
        articles = []
        articles.append({"title":u"今日战况","description":u"你今日消耗了%d千卡" % basic_tools.today_Calories(msg.source),"image":"http://wrist.ssast2015.com/static/img/data_today.jpg","url":"http://wrist.ssast2015.com/basic/today"})
        reply = ArticlesReply(articles=articles, message=msg)
    elif msg.key == "V1001_DATA_REPORT": #健康报告
        articles = []
        articles.append({"title":u"健康报告","description":u"运动趋势&健康报告","image":"http://wrist.ssast2015.com/static/img/data_report.jpg","url":"http://wrist.ssast2015.com/basic/report"})
        reply = ArticlesReply(articles=articles, message=msg)
    elif msg.key == "V1001_DATA_RANK": #排行榜
        articles = []
        articles.append({"title":u"排行榜","description":u"你今日消耗了%d千卡" % basic_tools.today_Calories(msg.source),"image":"http://wrist.ssast2015.com/static/img/data_rank.jpg","url":"http://wrist.ssast2015.com/basic/rank"})
        reply = ArticlesReply(articles=articles, message=msg)
    elif msg.key == "V1001_PLAN_MAKE":
        articles = []
        articles.append({"title":u"制定计划","description":u"快来制定你自己的运动计划吧!","image":"http://wrist.ssast2015.com/static/img/plan_make.jpg","url":"http://wrist.ssast2015.com/plan/make"})
        reply = ArticlesReply(articles=articles, message=msg)
    elif msg.key == "V1001_PLAN_OWN":
        articles = []
        articles.append({"title":u"查看我的","description":u"来看看你都有什么运动计划吧","image":"http://wrist.ssast2015.com/static/img/plan_own.jpg","url":"http://wrist.ssast2015.com/plan/own"})
        reply = ArticlesReply(articles=articles, message=msg)
    elif msg.key == "V1001_PLAN_SHARE":
        articles = []
        articles.append({"title":u"计划广场","description":u"想都想不到的运动计划","image":"http://wrist.ssast2015.com/static/img/plan_share.jpg","url":"http://wrist.ssast2015.com/plan/share"})
        reply = ArticlesReply(articles=articles, message=msg)
    elif msg.key == "V1001_PLAN_RANK":
        articles = []
        articles.append({"title":u"计划排行榜","description":u"来看看都有什么诱人的运动计划吧!","image":"http://wrist.ssast2015.com/static/img/plan_rank.jpg","url":"http://wrist.ssast2015.com/plan/rank"})
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
