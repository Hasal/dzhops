# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'saltstack.views',
    # Examples:
    # url(r'^$', 'dzhops.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^execute/$', 'remoteExecute', name='execute'),
    url(r'^api/execute/$', 'remoteExecuteApi', name='execute_api'),
)
