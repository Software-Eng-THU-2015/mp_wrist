from django.contrib import admin
from match.models import Match, MTag, MatchProgress

# Register your models here.
admin.site.register(Match)
admin.site.register(MTag)
admin.site.register(MatchProgress)
