# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'replacedata.views',
    # url(r'^$', 'oms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^repair/history/$', 'repairHistoryData', name='repair_data'),
    url(r'^api/history/$', 'repairHistoryDataAPI', name='repair_data_api'),
)
