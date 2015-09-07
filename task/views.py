from django.shortcuts import render

# Create your views here.
from task.forms import CreateTaskForm


def create_task(request):
    form = None
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            pass

    else:
        form = CreateTaskForm
    return render(request, 'task/create_task.html', {'form': form})
