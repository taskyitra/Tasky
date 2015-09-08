from django.shortcuts import render
from social.apps.django_app.default.models import UserSocialAuth

from task.models import Task



def index(request):
    tasks = Task.objects.all()
    ctx = {'tasks': tasks}  # Возвращаем контекст с данными для начальной страницы
    return render(request, 'base.html', ctx)
