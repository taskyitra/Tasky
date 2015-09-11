from django.conf.urls import patterns, include
from django.conf.urls import url

urlpatterns = patterns('user_account.views',
                       url(r'^generate_picture/$', 'generate_picture', name='generate_picture'),
                       url(r'^change_username/$', 'change_username', name='change_username'),
                       url(r'^user/(?P<pk>\d+)/$', 'user', name='user'),
                       )
