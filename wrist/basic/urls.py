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
import views

urlpatterns = [
    url(r'^get_session', views.get_session),
    url(r'^bind', views.bind),
    url(r'^redirect/profile', views.redirect_profile),
    url(r'^data/today', views.data_today),
    url(r'^data/rank', views.data_rank),
    url(r'^data/good', views.data_good),
    url(r'^data/friend', views.data_friend),
    url(r'^data/profile', views.data_profile),
    url(r'^add/friend', views.friend_add),
]
