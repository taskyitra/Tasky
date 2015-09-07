from django.shortcuts import render, redirect

# Create your views here.
from task.forms import CreateTaskForm, AnswerForm


def create_task(request):
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        answer_form = AnswerForm(request.POST)
        if form.is_valid() and answer_form.is_valid():
            try:
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                answer = answer_form.save(commit=False)
                answer.task = task
                answer.save()
                return redirect('/')
            except Exception as e:
                print(e)
    else:
        form = CreateTaskForm
        answer_form = AnswerForm
    return render(request, 'task/create_task.html', {'form': form, 'answer_form': answer_form})
