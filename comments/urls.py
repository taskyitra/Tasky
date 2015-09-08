from django.conf.urls import url, include, patterns

urlpatterns = patterns('comments.views',
                       url(r'^add/$', 'add', name='add_comment'),
                       )
