from django.shortcuts import render

# Create your views here.
from task.forms import CreateTaskForm


def create_task(request):
    form = None
    if request.POST:
        print('POST')
    else:
        form = CreateTaskForm
    return render(request, 'task/create_task.html', {'form': form})
