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
from match import urls as match_urls
from plan import urls as plan_urls
from basic import urls as basic_urls
from wechat import server

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^match/', include(match_urls)),
    url(r'^plan/', include(plan_urls)),
    url(r'^basic/', include(basic_urls)),
    url(r'^wechat/', server.handle),
]
