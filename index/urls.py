# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.views import login, logout

urlpatterns = patterns('index.views',
    # Examples:
    # url(r'^$', 'oms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login/$', login, name='login'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^upload/$', 'upload_file', name='upload'),
    url(r'^logout/$', logout, name='logout'),
)
