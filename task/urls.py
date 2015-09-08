from django.conf.urls import url, include, patterns

urlpatterns = patterns('task.views',
                       url(r'^create/$', 'create_task', name='create'),
                       url(r'^my_tasks/$', 'my_tasks', name='my_tasks'),
                       )
