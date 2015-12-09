import json
import urllib2
import urllib

def http_post(url, values):
        json_data = json.dumps(values)
        req = urllib2.Request(url=url, data=json_data)
        response = urllib2.urlopen(req)
        print response.read()

values = [{"distance": 0, "actTime": 0, "score": 2, "wakeNum": 0, "dsNum": 14, "calories": 0, "subType": 1, "nonActTime": 0, "wakeTimes": 0, "steps": 0, "user": 0, "startTime": "2015-11-10 00:00:00", "date": 20151110, "lsNum": 0, "endTime": "2015-11-10 00:14:00", "type": 1}]
http_post("http://wrist.ssast2015.com/bongdata/upload/?user=0&date=20151110", values)
