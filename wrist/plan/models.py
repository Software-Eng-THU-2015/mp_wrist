from django.db import models
from basic.models import User

# Create your models here.

class Plan(models.Model):
    name = models.CharField(max_length=30, default="")
    description = models.TextField(default="")
    createTime = models.IntegerField(default=0)
    startTime = models.IntegerField(default=0)
    endTime = models.IntegerField(default=0)
    goal = models.IntegerField(default=0)
    image = models.CharField(max_length=200, default="")
    owner = models.ForeignKey(User, related_name="user_plan_owner")
    members = models.ManyToManyField(User, related_name="user_plan_members")
    goods = models.IntegerField(default=0)
    finished = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

class PTag(models.Model):
    name = models.CharField(max_length=30,default="")
    plans = models.ManyToManyField(Plan, related_name="plan_ptag_plans")
  
    def __unicode__(self):
        return self.name
