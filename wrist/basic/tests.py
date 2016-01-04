import httplib, urllib
from django.test import TestCase
from basic.models import User
from wechat import tools as wechat_tools

# Create your tests here.

class TestUpdateUserData(TestCase):
    def setUp(self):
        self.user = User.objects.all()[0]
        self.value = [100,50,25,12]
    
    def test_update_height(self):
        conn = httplib.HTTPConnection(wechat_tools.domain[7:])
        conn.request("GET", "/basic/profile/data?userId=%d&type=0&value=%d" % (self.user.openId, self.value[0]))
        res = conn.getresponse()
        
        self.assertEqual(res.status, 200)
        self.assertEqual(res.reason, "OK")
        self.assertEqual(self.user.height, self.value[0])
    
    def test_update_weight(self):
        conn = httplib.HTTPConnection(wechat_tools.domain[7:])
        conn.request("GET", "/basic/profile/data?userId=%d&type=1&value=%d" % (self.user.openId, self.value[1]))
        res = conn.getresponse()
        
        self.assertEqual(res.status, 200)
        self.assertEqual(res.reason, "OK")
        self.assertEqual(self.user.weight, self.value[1])
    
    def test_update_dayPlan(self):
        conn = httplib.HTTPConnection(wechat_tools.domain[7:])
        conn.request("GET", "/basic/profile/data?userId=%d&type=2&value=%d" % (self.user.openId, self.value[2]))
        res = conn.getresponse()
        
        self.assertEqual(res.status, 200)
        self.assertEqual(res.reason, "OK")
        self.assertEqual(self.user.dayPlan, self.value[2])
    
    def test_update_sleepPlan(self):
        conn = httplib.HTTPConnection(wechat_tools.domain[7:])
        conn.request("GET", "/basic/profile/data?userId=%d&type=3&value=%d" % (self.user.openId, self.value[3]))
        res = conn.getresponse()
        
        self.assertEqual(res.status, 200)
        self.assertEqual(res.reason, "OK")
        self.assertEqual(self.user.sleepPlan, self.value[3])