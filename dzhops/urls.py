from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'dzhops.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'index.views.index', name='index'),
    url(r'^accounts/', include('index.urls')),
    url(r'^salt/', include('saltstack.urls')),
    url(r'^record/', include('record.urls')),
    url(r'^keys/', include('managekeys.urls')),
    url(r'^hostlist/', include('hostlist.urls')),
    url(r'^data/', include('replacedata.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/', include('newtest.urls')),
)
