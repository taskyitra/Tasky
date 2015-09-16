from __future__ import print_function
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image, ImageDraw, ImageOps, ImageFont
import cloudinary
from cloudinary.uploader import upload

from Tasky import settings
from task.models import Task, Solving
from user_account.models import UserProfile, Achievement, AchievementsSettings

from django.utils.translation import activate

cloudinary.config(
    cloud_name="dmt04dtgy",
    api_key="326982618723938",
    api_secret="fyssIAtgJ7g-LL1SsqjnLYSQgdc"
)


@login_required
def change_username(request):
    try:
        new_username = request.POST['value']
        if request.user.username == new_username:
            return HttpResponse(request.POST['value'], status=200)
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


def ach_gen(image, achievements, name, pos):
    ach = Achievement.objects.get(name=name)
    picture = Image.open(settings.BASE_DIR + ach.imageUrl)
    picture.thumbnail((100, 100))
    if not achievements.filter(achievement=ach).exists():
        picture = ImageOps.colorize(ImageOps.grayscale(picture), (0, 0, 0), (50, 50, 50))
    image.paste(picture, pos)


@login_required
def generate_picture(request):
    try:
        image = Image.new("RGB", (450, 470), color=(180, 180, 180))
        draw = ImageDraw.Draw(image)
        color = (94, 73, 15)
        username = ((10, 10), request.user.username)
        create = ((10, 50), "Создано задач: {}".format(Task.objects.count_tasks_for_user(request.user)))
        solved = ((10, 70), "Решено задач: {}".format(Solving.objects.count_solves_for_user(request.user)))
        percentage = (
            (10, 90), "Процент правильных ответов: {}%".format(Solving.objects.percentage_for_user(request.user)))
        rating = ((10, 110), "Рейтинг: {}".format(Solving.objects.rating_for_user(request.user)))
        header_font_size, statistic_font_size = 30, 15
        header_font = ImageFont.truetype("arial.ttf", header_font_size)
        statistic_font = ImageFont.truetype("arial.ttf", statistic_font_size)
        draw.text(username[0], username[1], fill=color, font=header_font)
        draw.text(create[0], create[1], fill=color, font=statistic_font)
        draw.text(solved[0], solved[1], fill=color, font=statistic_font)
        draw.text(percentage[0], percentage[1], fill=color, font=statistic_font)
        draw.text(rating[0], rating[1], fill=color, font=statistic_font)

        profile = UserProfile.objects.get_or_create_profile(request.user)
        achievements = AchievementsSettings.objects.filter(userProfile=profile)
        ach_first = Achievement.objects.get(name='First')
        first = Image.open(settings.BASE_DIR + ach_first.imageUrl)
        first.thumbnail((100, 100))
        if achievements.filter(achievement=ach_first).exists():
            image.paste(first, (340, 30))
            draw.text((430, 110), str(achievements.get(achievement=ach_first).count),
                      fill=(255, 0, 0), font=statistic_font)
        else:
            com = ImageOps.colorize(ImageOps.grayscale(first), (0, 0, 0), (50, 50, 50))
            image.paste(com, (340, 30))
        pictures_and_positions = (('Creator1', (10, 140)), ('Creator2', (120, 140)),
                                  ('Creator3', (230, 140)), ('Creator4', (340, 140)),
                                  ('Solver1', (10, 250)), ('Solver2', (120, 250)),
                                  ('Solver3', (230, 250)), ('Solver4', (340, 250)),
                                  ('Commentator1', (10, 360)), ('Commentator2', (120, 360)),
                                  ('Commentator3', (230, 360)), ('Commentator4', (340, 360)),)
        for pp in pictures_and_positions:
            ach_gen(image, achievements, pp[0], pp[1])
        path = 'user_account/static/user_account/pictures/other/im.png'
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
def user(request, pk):
    # activate('en')
    try:
        found_user = User.objects.get(pk=pk)
        profile = UserProfile.objects.get_or_create_profile(found_user)
        statistics = {'task_count': Task.objects.count_tasks_for_user(found_user),
                      'percentage': Solving.objects.percentage_for_user(found_user),
                      'rating': Solving.objects.rating_for_user(found_user),
                      'solved_task_count': Solving.objects.count_solves_for_user(found_user)}
        tasks = [{'task': task, 'tags': task.tags.all()} for task in Task.objects.filter(user=found_user)]
        achievements = [
            {'achieve': ach.achievement, 'count': ach.count,
             'is': ach.achievement.name == 'First'} for ach in
            AchievementsSettings.objects.filter(userProfile=profile)]
        solved_tasks = [{'task': solving.task, 'tags': solving.task.tags.all(),
                         'count': Solving.objects.attempts_count(found_user, solving.task)}
                        if solving.task else None  # {'task': None, 'tags': None,
                        #                       'count': Solving.objects.attempts_count(found_user, solving.task)}
                        for solving in Solving.objects.filter(user=found_user, is_solved=True)]
        print(solved_tasks)
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
    return render(request, 'user_account/user.html', {'founduser': found_user, 'profile': profile,
                                                      'statistic': statistics, 'tasks': tasks,
                                                      'achievements': achievements, 'solved_tasks': solved_tasks})
