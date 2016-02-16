# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('common.views',
    # Examples:
    # url(r'^$', 'oms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^key/list/$', 'salt_key_list', name='key_list'),
    url(r'^key/reject/$', 'salt_key_reject', name='key_reject'),
    url(r'^key/unaccept/$', 'salt_key_unaccept', name='key_unaccept'),
    url(r'^key/delete/$', 'salt_delete_key', name='key_delete'),
    url(r'^key/accept/$', 'salt_accept_key', name='key_accept'),
    url(r'^key/rejdelete/$', 'rejDeleteKey', name='key_rejdelete'),
    url(r'^module/deploy/$', 'module_deploy', name='module_deploy'),
    url(r'^module/update/$', 'module_update', name='module_update'),
    url(r'^routine/maintenance/$', 'routine_maintenance', name='routine_maintenance'),
    url(r'^remote/execution/$', 'remote_execution', name='remote_execution'),
    url(r'^record/$', 'record', name='record'),
    url(r'^record/detail/$', 'recordDetail', name='record_detail'),
    url(r'^host/data/coll/$', 'hostDataCollection', name='host_data_coll'),
    url(r'^data/collection/$', 'dataCollection', name='data_collection'),
)
