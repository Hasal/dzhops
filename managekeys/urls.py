# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'managekeys.views',
    # Examples:
    # url(r'^$', 'dzhops.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^show/$', 'manageMinionKeys', name='keys_show'),
    url(r'^api/$', 'manageMinionKeysAPI', name='keys_api'),
    url(r'^(?P<action>accept|delete|reject)/$', 'actionMinionKeys', name='action_keys'),
)