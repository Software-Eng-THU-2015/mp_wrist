from django.contrib import admin
from plan.models import Plan, PTag, PlanProgress

# Register your models here.
admin.site.register(Plan)
admin.site.register(PTag)
admin.site.register(PlanProgress)
