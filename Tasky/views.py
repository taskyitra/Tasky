from django.contrib.auth.models import User
from django.shortcuts import render

from task.models import Task
from user_account.models import UserProfile


def index(request):
    tasks = Task.objects.all()
    ctx = {'tasks': tasks}  # Возвращаем контекст с данными для начальной страницы
    return render(request, 'base.html', ctx)
