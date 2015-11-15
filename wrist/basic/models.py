from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=200, default="")
    sex = models.IntegerField()
    openId = models.CharField(max_length=150)
    goods = models.IntegerField()  
    
    def __unicode__(self):
        return self.name
  
class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="basic_team")
    goods = models.IntegerField()

    def __unicode__(self):
        return self.name

class Data(models.Model):
    user = models.ForeignKey(User, related_name="basic_data")
    startTime = models.CharField(max_length = 30)
    endTime = models.CharField(max_length = 30)
    type = models.IntegerField(default=0)
    subType = models.IntegerField(default=0)
    distance = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    calories = models.IntegerField(default=0)
    steps = models.IntegerField(default=0)
    actTime = models.IntegerField(default=0)
    nonActTime = models.IntegerField(default=0)
    dsNum = models.IntegerField(default=0)
    lsNum = models.IntegerField(default=0)
    wakeNum = models.IntegerField(default=0)
    wakeTimes = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s:%s %s" % (self.user.name, self.startTime, self.endTime)

