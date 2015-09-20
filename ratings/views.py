from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from task.models import Task, Answer, Solving, Rating, Tag
from user_account.models import UserProfile


def task_rating(request):
    info = []
    tasks = Task.objects.all()
    for task in tasks:
        info.append(task.task_statistics)
    return render(request, 'ratings/task_rating.html', {'info': info})


def user_rating(request):
    user_info = []
    for user in User.objects.all():
        profile = UserProfile.objects.get_or_create_profile(user)
        user_info.append(profile.statistics())
    return render(request, 'ratings/user_rating.html', {'info': user_info})
