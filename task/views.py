from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.forms.forms import NON_FIELD_ERRORS

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
                return redirect('/')
            except Exception as e:
                print(e)
    else:
        form = CreateTaskForm
        answer_form = AnswerForm
    return render(request, 'task/create_task.html', {'form': form, 'answer_form': answer_form})


@login_required
def edit(request, pk):
    return render(request, 'task/edit.html')


@login_required
def my_tasks(request):
    user_tasks = Task.objects.filter(user=request.user)
    print(user_tasks)
    return render(request, 'task/my_tasks.html', {'tasks': user_tasks})


@login_required
def solve_task(request, pk):
    try:
        task = Task.objects.filter(pk=pk).first()
    except Exception as e:
        print('Такой задачи не существует')
        return redirect('/')

    is_old_solving = True if len(Solving.objects.filter(task=task).filter(user=request.user) \
                                 .filter(is_solved=True)) > 0 else False
    if is_old_solving:
        return redirect('/')  # Если задача уже была решена

    if request.method == 'POST':
        print('POST')
        form = AnswerForm(request.POST)
        if form.is_valid():
            try:
                answer = form.save(commit=False).text
                right_answer = Answer.objects.filter(task=task).filter(text=answer)
                if len(right_answer) == 0:
                    solving = Solving(user=request.user, task=task, is_solved=False)
                    solving.save()
                    form.full_clean()
                    form._errors[NON_FIELD_ERRORS] = form.error_class(['Неправильный ответ'])
                else:
                    solving = Solving(user=request.user, task=task, is_solved=True)
                    solving.save()
                    return redirect('/')
            except Exception as e:
                print(e)
    else:
        form = AnswerForm
    return render(request, 'task/solve.html', {'form': form, 'task': task})
