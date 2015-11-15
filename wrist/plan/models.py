from django.db import models
from basic.models import User

# Create your models here.

class Plan(models.Model):
    name = models.CharField(max_length=30)
    starttime = models.CharField(max_length=30)
    endtime = models.CharField(max_length=30)
    goal_0 = models.IntegerField()
    goal_1 = models.IntegerField()
    goal_2 = models.IntegerField()
    owner = models.ForeignKey(User, related_name="owner_plan")
    members = models.ManyToManyField(User, related_name="members_plan")
    goods = models.IntegerField()

    def __unicode__(self):
        return self.name
