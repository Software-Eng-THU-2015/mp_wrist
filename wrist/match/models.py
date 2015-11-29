from django.db import models
from basic.models import User, Team

# Create your models here.

class Match(models.Model):
    creator = models.ForeignKey(User, related_name="user_match")
    members = models.ManyToManyField(Team, related_name = "team_match")
    title = models.CharField(max_length=100, default="")
    description = models.TextField(default="")
    goal = models.IntegerField(default=0)
    goods = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title