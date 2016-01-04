from django.contrib import admin
from basic.models import User, Team, Data, DayData, Good, Archive, PreFriend

# Register your models here.
admin.site.register(User)
admin.site.register(Team)
admin.site.register(Data)
admin.site.register(DayData)
admin.site.register(Good)
admin.site.register(Archive)
admin.site.register(PreFriend)