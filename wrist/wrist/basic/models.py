from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=200, default="")
    sex = models.IntegerField(default=0)
    openId = models.CharField(max_length=150)
    goods = models.IntegerField(default=0)  
    level = models.IntegerField(default=0)
    uid = models.CharField(max_length=100, default="")
    
    def __unicode__(self):
        return self.name
  
class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="user_team")
    type = models.IntegerField(default=0)
    goods = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

class Data(models.Model):
    user = models.ForeignKey(User, related_name="user_data")
    date = models.IntegerField()
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

class DayDate(models.Model):
    user = models.ForeignKey(User, related_name="user_daydata")
    date = models.IntegerField()
    steps = models.IntegerField(default=0)
    calories = models.IntegerField(default=0)
    sleep = models.IntegerField(default=0)
    distance = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s:%d" % (self.user.name, self.date)

class Archive(models.Model):
    name = models.CharField(max_length = 100)
    owners = models.ManyToManyField(User, related_name="user_archive")

    def __unicode__(self):
        return self.name
