from django.conf.urls import url, include, patterns

urlpatterns = patterns('task.views',
                       url(r'^create/$', 'create_task', name='create'),
                       url(r'^edit/(?P<pk>\d+)/$', 'edit', name='edit'),
                       url(r'^my_tasks/$', 'my_tasks', name='my_tasks'),
                       url(r'^solve_task/(?P<pk>\d+)/$', 'solve_task', name='solve_task'),
                       )
