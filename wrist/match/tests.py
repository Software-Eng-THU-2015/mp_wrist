import httplib, urllib
from django.test import TestCase
from match.models import Match
from basic.models import User
from wechat import tools as wechat_tools

# Create your tests here.

class TestUpdateUserData(TestCase):
    def setUp(self):
        self.user = User.objects.all()[0]
        self.data = {
        "match_name": u"测试比赛_名字",
        "begintime": u"2016-01-01 10:10",
        "endtime": u"2016-01-04 10:10",
        "tag0": u"测试_比赛_标签_0",
        "tag1": u"测试_比赛_标签_1",
        "tags": u"测试_比赛_标签_left",
        "friend0": self.user.openId,
        "opponent0": self.user.openId,
        "comment": u"测试_比赛_描述"
        }
        self.ld = Match.objects.all().count()
        conn = httplib.HTTPConnection(wechat_tools.domain[7:])
        params = urllib.urlencode({
        "userId":self.user.openId,
        "match_name":self.data["match_name"],
        "begintime":self.data["begintime"],
        "endtime":self.data["endtime"],
        "tag0":self.data["tag0"],
        "tag1":self.data["tag1"],
        "tags":self.data["tags"],
        "friend0":self.data["friend0"],
        "opponent0":self.data["opponent0"],
        "comment":self.data["comment"]})
        headers = {"Content-type": "application/x-www-form-urlencode"}
        conn.request("POST","/plan/submit/make",params,headers)
        res = conn.getresponse()
    
    def test_plan_create(self):
        self.assertEqual(self.ld+1, Match.objects.all().count())
        