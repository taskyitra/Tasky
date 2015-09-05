from django.conf.urls import patterns, url

__author__ = 'Stanislau'

urlpatterns = patterns('account.views',
                       url(r'^login/$', 'login', name='login'),
                       url(r'^signin/$', 'signin', name='signin'),
                       url(r'^logout/$', 'logoutUser', name='logout'),
                       )
