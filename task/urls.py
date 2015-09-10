from django.conf.urls import url, include, patterns

urlpatterns = patterns('task.views',
                       url(r'^create/$', 'create_task', name='create'),
                       url(r'^edit/(?P<pk>\d+)/$', 'edit', name='edit'),
                       url(r'^my_tasks/$', 'my_tasks', name='my_tasks'),
                       url(r'^put_mark_for_task/$', 'put_mark_for_task', name='put_mark_for_task'),
                       url(r'^solve_task/(?P<pk>\d+)/$', 'solve_task', name='solve_task'),
                       url(r'^create_task_success/(?P<pk>\d+)/$', 'create_task_success', name='create_task_success'),
                       url(r'^getOptionsTypeahead/(?P<query>.+)$', 'getOptionsTypeahead', name='getOptionsTypeahead'),
                       )
