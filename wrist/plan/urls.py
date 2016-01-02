"""wrist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from plan import views

urlpatterns = [
    url(r'^redirect', views.redirect_plan),
    url(r'^data/make', views.plan_make),
    url(r'^data/own', views.plan_own),
    url(r'^data/square', views.plan_square),
    url(r'^data/rank', views.plan_rank),
    url(r'^submit/make', views.submit_make),
    url(r'^data/follow', views.plan_follow),
]
