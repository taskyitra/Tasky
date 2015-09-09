from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.forms.forms import NON_FIELD_ERRORS
from comments.models import Comment

from task.forms import CreateTaskForm, AnswerForm
from task.models import Task, Answer, Solving


@login_required
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
                return redirect('/task/my_tasks/')
            except Exception as e:
                print(e)
    else:
        form = CreateTaskForm
        answer_form = AnswerForm
    return render(request, 'task/create_task.html', {'form': form, 'answer_form': answer_form})


@login_required
def edit(request, pk):
    task = Task.objects.filter(pk=pk).first()
    answer = Answer.objects.filter(task=task).first()  # Здесь должны быть все
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        answer_form = AnswerForm(request.POST)
        if form.is_valid() and answer_form.is_valid():
            try:
                task = form.save(commit=False)
                task.user = request.user
                task.pk = pk
                task.creation_date = Task.objects.filter(pk=pk).first().creation_date
                task.save()
                Answer.objects.filter(task=task).delete()
                answer = answer_form.save(commit=False)
                answer.task = task
                answer.save()
            except Exception as e:
                print(e)
    else:
        form = CreateTaskForm(instance=task)
        answer_form = AnswerForm(instance=answer)
    return render(request, 'task/edit.html', {'form': form, 'answer_form': answer_form})


@login_required
def my_tasks(request):
    user_tasks = Task.objects.filter(user=request.user)
    return render(request, 'task/my_tasks.html', {'tasks': user_tasks})


@login_required
def solve_task(request, pk):
    task = Task.objects.filter(pk=pk).first()
    comments = Comment.objects.filter(task=task)
    is_old_solving = True if len(Solving.objects.filter(task=task).filter(user=request.user) \
                                 .filter(is_solved=True)) > 0 else False
    if is_old_solving:
        return render(request, 'task/solve.html', {'form': None, 'task': task, 'is_old_solving': is_old_solving,
                                                   'comments': comments})
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            try:
                answer = form.save(commit=False).text
                right_answer = Answer.objects.filter(task=task).filter(text=answer)
                if len(right_answer) == 0:
                    solving = Solving(user=request.user, task=task, is_solved=False, level=task.level)
                    solving.save()
                    form.full_clean()
                    form._errors[NON_FIELD_ERRORS] = form.error_class(['Неправильный ответ'])
                else:
                    solving = Solving(user=request.user, task=task, is_solved=True, level=task.level)
                    solving.save()
                    return render(request, 'task/solve.html', {'form': None, 'task': task, 'is_old_solving': False,
                                                               'comments': comments})
            except Exception as e:
                print(e)
    else:
        form = AnswerForm
    return render(request, 'task/solve.html', {'form': form, 'task': task,
                                               'comments': comments})
