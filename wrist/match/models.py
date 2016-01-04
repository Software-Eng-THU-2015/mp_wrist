from django.db import models
from basic.models import User, Team

# Create your models here.

class Match(models.Model):
    creator = models.ForeignKey(User, related_name="user_match_creator")
    members = models.ManyToManyField(Team, related_name = "team_match_members")
    user_members = models.ManyToManyField(User, related_name = "user_match_members")
    createTime = models.IntegerField(default=0)
    title = models.CharField(max_length=100, default="")
    description = models.TextField(default="")
    startTime = models.IntegerField(default=0)
    endTime = models.IntegerField(default=0)
    image = models.CharField(max_length=200, default="")
    finished = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class MTag(models.Model):
    name = models.CharField(max_length=30, default="")
    matchs = models.ManyToManyField(Match, related_name = "match_mtag_matchs")

    def __unicode__(self):
        return self.name
