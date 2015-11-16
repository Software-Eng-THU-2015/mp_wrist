#-*- coding=utf-8 -*-
###
# description: 微信API
###

__author__ = "chendaxixi"

import hashlib
import httplib
import requests
import base64
import json
#import qrcode  #QRCode模块，用于生成二维码，似乎不太好装，有需求的同学自己装PIL,qrcode库再用吧
from wechatpy.utils import to_text, to_binary
from wechatpy.client import WeChatClient

APP_ID = ""
APP_SECRET = ""
TOKEN = ""
client = WeChatClient(APP_ID, APP_SECRET)
DEVICE_BASE_URL = 'https://api.weixin.qq.com/device/'
MEDIA_BASE_URL = "https://api.weixin.qq.com/cgi-bin/media/"
tmp_media_id = None

#校验签名是否正确
def checkSignature(request):
    try:
        sign = request.GET["signature"]
        timestamp = request.GET["timestamp"]
        nonce = request.GET["nonce"]
    except:
	return False

    token = TOKEN
    tmp = [timestamp, nonce, token]
    tmp.sort()
    res = tmp[0] + tmp[1] + tmp[2]
    m = hashlib.sha1(res)
    return m.hexdigest() == sign

#获取海思力Token
def getToken():
    conn = httplib.HTTPConnection("wx.chendaxixi.me")
    conn.request("GET", "/token")
    return conn.getresponse().read()    

#创建菜单，传入一个dict
def menuCreate(body):
    client.menu.delete()
    return client.menu.create(body)

#查询菜单
def menuQuery():
    return client.menu.get()

#删除当前菜单
def menuDelete():
    return client.menu.delete()

def POST(url, foot, data, params, files=None):
    tmp = "access_token=%s" % params["access_token"]
    for item in params:
        if not item == "access_token":
            tmp += "&%s=%s" % (item, params[item]) 
    res = requests.request(method="post", url="%s%s?%s" % (url, foot, tmp), 
       data=data, files=files)
    res.encoding = 'utf-8'
    return res.json()    

#上传媒体文件，type=image,voice,video,thumb;返回信息为一个JSON数组，若成功，在res["media_id"]中获得media_id,有效期为三天
def uploadMedia(type, filename):
    res = POST(MEDIA_BASE_URL, "upload", {"media": file(filename)}, {"access_token": client.fetch_access_token()["access_token"], "type": type}, {filename:(filename,open(filename,'rb'))})   
    return res

#发送客服文本信息，user为openid
def customSendText(user, content):
    return client.message.send_text(user, content)

#发送客服图片信息，指定filename或者mediaId
def customSendImage(user, filename, mediaId=None):
    if mediaId:
        return client.message.send_image(user, mediaId)
    res =  updateMedia("image", filename)
    try:
        return client.message.send_image(user, res["media_id"])
    except:
        return res

#发送客服语音信息
def customSendVoice(user, mediaId):
    return client.message.send_voice(user, mediaId)

#发送客服视频信息
def customSendVideo(user, mediaId, title=None, description=None):
    return client.message.send_video(user, mediaId, title, description)

#发送客服图文信息，四个参数分别为:标题、概述、图片的url地址，点击后链接的url地址
def customSendArticle(user, title, description, image, url):
    return client.message.send_articles(user, [{"title":title,"description":description,"image":image,"url":url}])

#发送客服多图文信息
def customSendArticles(user, articles):
    return client.message.send_articles(user, articles)

#查询硬件状态
def getStat(deviceId):
    return POST(DEVICE_BASE_URL, "get_stat", {"device_id":deviceId}, {"access_token": getToken()})

#查询设备绑定的用户id
def getOpenId(deviceType, deviceId):
    return POST(DEVICE_BASE_URL, "get_openid", {"device_type":deviceType,"device_id":deviceId}, {"access_token": getToken()})
   
#给设备发信息
def transMsg(deviceType, deviceId, user, content):
    content = to_text(base64.b64encode(to_binary(content)))
    return POST(DEVICE_BASE_URL, "transmsg", {"device_type":deviceType,"device_id":deviceId,"openid":user,"content":content}, {"access_token": getToken()})

#生成二维码(一个ticket)
def createQrCode(deviceId, filename):
    return POST(DEVICE_BASE_URL, "create_qrcode", json.dumps({"device_num": 1, "device_id_list":[deviceId]}), {"access_token": getToken()})

#生成二维码图片，装有PIL,qrcode后可使用
#def createQrByDeviceId(deviceId, filename):
#    res = POST(DEVICE_BASE_URL, "create_qrcode", json.dumps({"device_num": 1, "device_id_list":[deviceId]}), {"access_token": getToken()})
#    try:
#        ticket = res["code_list"][0]["ticket"]
#        img = qrcode.make(ticket)
#        img.save(filename)
#        return ticket
#    except:
#        return res

if __name__ == "__main__":
    print "python-wechat tools modified by chendaxixi"   
