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
    url(r'^deploy/$', 'deployProgram', name='deploy'),
    url(r'^update/$', 'updateConfig', name='update'),
    url(r'^routine/$', 'routineMaintenance', name='routine'),
    url(r'^api/execute/$', 'remoteExecuteApi', name='execute_api'),
    url(r'^api/deploy/$', 'deployProgramApi', name='deploy_api'),
)
