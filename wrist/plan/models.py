from django.db import models
from basic.models import User

# Create your models here.

class Plan(models.Model):
    name = models.CharField(max_length=30, default="")
    description = models.TextField(default="")
    createTime = models.CharField(max_length=30)
    starttime = models.CharField(max_length=30)
    endtime = models.CharField(max_length=30)
    goal_0 = models.IntegerField(default=0)
    goal_1 = models.IntegerField(default=0)
    goal_2 = models.IntegerField(default=0)
    images = models.TextField(default="")
    owner = models.ForeignKey(User, related_name="owner_plan")
    members = models.ManyToManyField(User, related_name="members_plan")
    goods = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30)
    plans = models.ManyToManyField(Plan, related_name="plan_tag")

    def __unicode__(self):
        return self.name


