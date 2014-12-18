from django.conf.urls import patterns, include, url
from django.contrib import admin

from cine import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cine.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<title>\w+_\w+$)', views.index, name='index'),
)
