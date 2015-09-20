from django.shortcuts import render
from social.apps.django_app.default.models import UserSocialAuth
from django.contrib.auth.models import User
from task.models import Task, Answer, Solving, Rating, Tag
from collections import Counter

from task.models import Task


# def index(request):
#     tasks = Task.objects.all()
#     ctx = {'tasks': tasks}  # Возвращаем контекст с данными для начальной страницы
#     return render(request, 'base.html', ctx)


def get_hardest_tasks(tasks):
    hardest_tasks = []
    for task in tasks:
        solutions = Solving.objects.filter(task=task)
        accepted = len(solutions.filter(is_solved=True))
        accuracy = accepted / max(len(solutions), 1)
        hardest_tasks.append((task, accuracy, len(solutions)))
    hardest_tasks.sort(key=lambda task_: task_[2], reverse=True)
    hardest_tasks.sort(key=lambda task_: task_[1])
    hardest_tasks = hardest_tasks[:5]
    return [(task[0], int(100*task[1])) for task in hardest_tasks]


def get_best_users():
    right_solutions = Solving.objects.filter(is_solved=True)
    users = []
    for solution in right_solutions:
        users.append(solution.user)
    return Counter(users).most_common(5)


def index(request):
    tasks = Task.objects.all()
    newest_tasks = reversed(tasks[len(tasks)-5:])
    hardest_tasks = get_hardest_tasks(tasks)
    tags = Tag.objects.all()
    users = get_best_users()
    info = {'newest_tasks': newest_tasks, 'hardest_tasks': hardest_tasks, 'tags': tags, 'users': users}
    return render(request, 'homeindex.html', info)

