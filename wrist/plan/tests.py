import httplib, urllib
from django.test import TestCase
from plan.models import Plan
from basic.models import User
from wechat import tools as wechat_tools

# Create your tests here.

class TestUpdateUserData(TestCase):
    def setUp(self):
        self.user = User.objects.all()[0]
        self.data = {
        "plan_name": u"测试计划_名字",
        "begintime": u"2016-01-01 10:10",
        "endtime": u"2016-01-04 10:10",
        "goal": 10000,
        "tag0": u"测试_计划_标签_0",
        "tag1": u"测试_计划_标签_1",
        "tags": u"测试_计划_标签_left",
        "friend0": self.user.openId,
        "comment": u"测试_计划_描述"
        }
        self.ld = Plan.objects.all().count()
        
        conn = httplib.HTTPConnection(wechat_tools.domain[7:])
        params = urllib.urlencode({
        "userId":self.user.openId,
        "plan_name":self.data["plan_name"],
        "begintime":self.data["begintime"],
        "endtime":self.data["endtime"],
        "goal":self.data["goal"],
        "tag0":self.data["tag0"],
        "tag1":self.data["tag1"],
        "tags":self.data["tags"],
        "friend0":self.data["friend0"],
        "comment":self.data["comment"]})
        headers = {"Content-type": "application/x-www-form-urlencode"}
        conn.request("POST","/plan/submit/make",params,headers)
        res = conn.getresponse()
    
    def test_plan_create(self):
        self.assertEqual(self.ld+1, Plan.objects.all().count())
        