from django.conf.urls import url, include, patterns

urlpatterns = patterns('ratings.views',
                       url(r'^user_rating/$', 'user_rating', name='user_rating'),
                       url(r'^task_rating/$', 'task_rating', name='task_rating'),
                       )