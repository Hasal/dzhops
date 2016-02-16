from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dzhops.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'index.views.index', name='index'),
    url(r'^accounts/', include('index.urls')),
    url(r'^common/', include('common.urls')),
    url(r'^hostlist/', include('hostlist.urls')),
    url(r'^data/', include('replacedata.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
