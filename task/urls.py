from django.conf.urls import url, include, patterns
# from task.views import TasksByTag

urlpatterns = patterns('task.views',
                       url(r'^create/$', 'create_task', name='create'),
                       url(r'^edit/(?P<pk>\d+)/$', 'edit', name='edit'),
                       url(r'^delete/$', 'delete_task', name='delete_task'),
                       url(r'^put_mark_for_task/$', 'put_mark_for_task', name='put_mark_for_task'),
                       url(r'^solve_task/(?P<pk>\d+)/$', 'solve_task', name='solve_task'),
                       url(r'^create_task_success/(?P<pk>\d+)/$', 'create_task_success', name='create_task_success'),
                       url(r'^getOptionsTypeahead/(?P<query>.+)$', 'get_options_typeahead', name='getOptionsTypeahead'),
                       url(r'^tasks_by_tag/(?P<tag>.+)$', 'tasks_by_tag', name='tasks_by_tag'),
                    #   url(r'^tasks_by_tag/(?P<tag>.+)$', TasksByTag.as_view(), name='tasks_by_tag'),
                       url(r'^add_picture/$', 'add_picture', name='add_picture'),
                       )
