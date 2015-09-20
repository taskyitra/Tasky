from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from task.models import Task


def redirect_edit(func):
    def _view(request, *args, **kwargs):
        if Task.objects.get(pk=kwargs['pk']).user != request.user:
            return redirect(reverse('task:solve_task', kwargs={'pk': kwargs['pk']}))
        return func(request, kwargs['pk'])
    return _view
