# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('hostlist.views',
    # Examples:
    # url(r'^$', 'oms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^list/$', 'host_list', name='host_list'),
    url(r'^list/engineer/$', 'engineerList', name='engineer_list'),
    url(r'^showlist/$', 'showList', name='show_list'),
    #url(r'^add/$', 'host_list_manage', name='host_add'),
    #url(r'^delete/$', 'host_list_manage', name='host_delete'),
    #url(r'^manage/(?P<id>\d+)/$', 'host_list_manage', name='host_manage'),
)
