# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('common.views',
    # Examples:
    # url(r'^$', 'oms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^key/list/$', 'salt_key_list', name='key_list'),
    url(r'^key/delete/$', 'salt_delete_key', name='key_delete'),
    url(r'^key/accept/$', 'salt_accept_key', name='key_accept'),
    url(r'^module/deploy/$', 'module_deploy', name='module_deploy'),
    url(r'^module/update/$', 'module_update', name='module_update'),
    url(r'^remote/execution/$', 'remote_execution', name='remote_execution'),
)
