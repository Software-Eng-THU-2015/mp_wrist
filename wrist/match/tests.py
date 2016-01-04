import httplib, urllib
from django.test import TestCase
from match.models import Match
from basic.models import User
from wechat import tools as wechat_tools

# Create your tests here.

class TestUpdateUserData(TestCase):
    def setUp(self):
        self.user = User(openId="ose6Ut8Ir-41wB7gQx89BifYa49Q",name="test")
        self.user.save()
        self.data = {
        "match_name": "test_name",
        "begintime": u"2016-01-01 10:10",
        "endtime": u"2016-01-04 10:10",
        "goal": 10000,
        "tag0": "test_tag_0",
        "tag1": "test_tag_1",
        "tags": "test_tag_s",
        "friend0": self.user.openId,
        "opponent0": self.user.openId,
        "comment": "test_comment"
        }=
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
        self.assertEqual(1, Match.objects.all().count())
        