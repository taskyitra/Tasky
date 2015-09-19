from __future__ import print_function
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
import cloudinary
from cloudinary.uploader import upload

from task.models import Task, Solving
from user_account.models import UserProfile, AchievementsSettings
from user_account.utils import generate_picture_from_user_info

# cloudinary.config(
#     cloud_name="dmt04dtgy",
#     api_key="326982618723938",
#     api_secret="fyssIAtgJ7g-LL1SsqjnLYSQgdc"
# )


@login_required
def change_username(request):
    try:
        new_username = request.POST['value']
        if request.user.username == new_username:
            return HttpResponse(new_username, status=200)
        if User.objects.filter(username=new_username).exists():
            new_username = request.user.username
        else:
            current_user = request.user
            current_user.username = new_username
            current_user.save()
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
    return HttpResponse(new_username, status=200)


@login_required
def generate_picture(request):
    try:
        path = 'user_account/static/user_account/pictures/other/im.png'
        profile = UserProfile.objects.get_or_create_profile(request.user)
        image = generate_picture_from_user_info(
            request.user.username, profile.statistics(),
            AchievementsSettings.objects.filter(userProfile=profile)
        )
        image.save(path, "PNG")
        file = upload(path)
        imageUrl = file['url']
        profile.pictureUrl = imageUrl
        profile.save()
        os.remove(path)
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
    return HttpResponse(imageUrl, status=200)


@login_required
def change_locale(request):
    if request.method == 'POST':
        profile = UserProfile.objects.get_or_create_profile(request.user)
        profile.locale = int(request.POST['locale'])
        profile.save()
    return HttpResponse(status=200)


@login_required
def user(request, pk):
    try:
        found_user = User.objects.get(pk=pk)
        profile = UserProfile.objects.get_or_create_profile(found_user)
        statistics = profile.statistics()
        tasks = [{'task': task, 'tags': task.tags.all()} for task in Task.objects.filter(user=found_user)]
        achievements = AchievementsSettings.objects.get_achievements_for_user(found_user)
        solved_tasks = Solving.objects.solved_tasks_for_user(found_user)
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
    return render(request, 'user_account/user.html',
                  {'founduser': found_user, 'profile': profile, 'statistic': statistics,
                   'tasks': tasks, 'achievements': achievements, 'solved_tasks': solved_tasks})
