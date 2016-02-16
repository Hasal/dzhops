# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('replacedata.views',

    # url(r'^$', 'oms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^replace/history/$', 'dataReplaceHistory', name='replace_data'),
    url(r'^replace/all/$', 'dataReplaceAll', name='replace_data_all'),
)
