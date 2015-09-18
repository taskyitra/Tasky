import json
import os
from io import BytesIO
import base64
from gettext import gettext as _

from PIL import Image
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.forms.forms import NON_FIELD_ERRORS
import cloudinary
from cloudinary.uploader import upload

from comments.models import Comment
from task.decorators import redirect_edit, redirect_solve
from task.forms import AnswerForm
from task.models import Task, Answer, Solving, Rating, Tag
from user_account.models import UserProfile, Achievement, AchievementsSettings

cloudinary.config(
    cloud_name="dmt04dtgy",
    api_key="326982618723938",
    api_secret="fyssIAtgJ7g-LL1SsqjnLYSQgdc"
)


def set_achievements_at_creation(user):
    achivements_names = {5: 'Creator1', 10: 'Creator2', 20: 'Creator3', 30: 'Creator4'}
    count = Task.objects.count_tasks_for_user(user)
    if count in achivements_names.keys():
        profile = UserProfile.objects.get_or_create_profile(user)
        achievement = Achievement.objects.get(name=achivements_names[count])
        if not AchievementsSettings.objects.filter(userProfile=profile, achievement=achievement).exists():
            AchievementsSettings.objects.create(userProfile=profile, achievement=achievement, count=1)


def set_achievements_at_decision(user, task):
    achivements_names = {5: 'Solver1', 10: 'Solver2', 20: 'Solver3', 30: 'Solver4'}
    count = Solving.objects.count_solves_for_user(user)
    if count in achivements_names.keys():
        profile = UserProfile.objects.get_or_create_profile(user)
        achievement = Achievement.objects.get(name=achivements_names[count])
        if not AchievementsSettings.objects.filter(userProfile=profile, achievement=achievement).exists():
            AchievementsSettings.objects.create(userProfile=profile, achievement=achievement, count=1)
    if Solving.objects.is_first_solving(task):
        profile = UserProfile.objects.get_or_create_profile(user)
        achievement = Achievement.objects.get(name='First')
        AchievementsSettings.objects.increment_counter(profile, achievement)


@login_required
def create_task(request):
    if request.method == 'POST':
        try:
            json_obj = json.loads(request.POST['task'])
            task = Task.objects.create_task_from_fields(json_obj, request.user)
            set_achievements_at_creation(request.user)
            return HttpResponse(task.pk, status=200)
        except ValueError as e:
            print()
            return HttpResponse(status=500)
    return render(request, 'task/create_task.html')


@login_required
@redirect_edit
def edit(request, pk):
    task = Task.objects.get(pk=pk)
    try:
        if request.method == 'POST':
            json_obj = json.loads(request.POST['task'])
            task.edit_task_from_fields(json_obj)
            return HttpResponse(status=200)
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
    answers = [{'val': x.text, 'num': i} for i, x in enumerate(Answer.objects.filter(task=task))]
    tags = [{'val': x.tag_name, 'num': i} for i, x in enumerate(task.tags.all())]
    return render(request, 'task/edit.html', {'task': task, 'answers': answers, 'tags': tags})


@login_required
@redirect_solve
def solve_task(request, pk):
    task = Task.objects.get(pk=pk)
    if Solving.objects.filter(task=task, user=request.user, is_solved=True).exists():
        return render_solve_page(request, None, task, True)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            if not Answer.objects.filter(task=task, text=form.save(commit=False).text).exists():
                solving = Solving(user=request.user, task=task, is_solved=False, level=task.level)
                solving.save()
                form.full_clean()
                if UserProfile.objects.get_or_create_profile(request.user).locale == 0:
                    form._errors[NON_FIELD_ERRORS] = form.error_class(['Неправильный ответ'])
                else:
                    form._errors[NON_FIELD_ERRORS] = form.error_class(['Wrong answer'])
            else:
                solving = Solving(user=request.user, task=task, is_solved=True, level=task.level)
                solving.save()
                set_achievements_at_decision(request.user, task)
                return render_solve_page(request, None, task, False)
    else:
        form = AnswerForm
    return render_solve_page(request, form, task, False)


def render_solve_page(request, form, task, is_old_solving):
    did_he_put_mark = Rating.objects.did_he_put_mark(request.user, task)
    func = lambda x: x if x is not None else '/static/user_account/pictures/unknown.png'
    comments = [{'comment': comment, 'url':
                func(UserProfile.objects.get_or_create_profile(comment.user).pictureUrl)}
                for comment in Comment.objects.filter(task=task)]
    return render(request, 'task/solve.html', {'form': form, 'task': task, 'is_old_solving': is_old_solving,
                                               'comments': comments, 'did_user_put': did_he_put_mark,
                                               'tags': task.tags.all(), 'statistics': task.task_statistics()})


@login_required
def put_mark_for_task(request):
    average_rating = 0
    if request.method == 'POST':
        try:
            json_obj = json.loads(request.POST['data'])
            average_rating = Rating.objects.put_rating_from_fields(json_obj)
        except ValueError as e:
            print(e)
            return HttpResponse(status=500)
    return HttpResponse(average_rating, status=200)


@login_required
def create_task_success(request, pk):
    return render(request, 'task/create_task_success.html',
                  {'task': Task.objects.get(pk=pk)})


def get_options_typeahead(request, query):
    data = []
    for tag in Tag.objects.all():
        if query in tag.tag_name:
            data.append({'value': tag.tag_name})
    return JsonResponse(data, safe=False, status=200)


def add_picture(request):
    if request.method == 'POST':
        try:
            json_str = request.POST['content'].split(',')[1]
            image = Image.open(BytesIO(base64.b64decode(json_str)))
            path = 'user_account/static/user_account/pictures/other/im.png'
            image.save(path, "PNG")
            imageUrl = upload(path)['url']
            os.remove(path)
            return HttpResponse(imageUrl, status=200)
        except Exception as e:
            print(e)
            return HttpResponse(status=500)
    return HttpResponse(status=200)


def delete_task(request):
    if request.method == 'POST':
        try:
            pk = str(request.POST['pk'])
            task = Task.objects.get(pk=pk)
            if request.user != task.user:
                raise Exception()
            task.delete()
        except Exception as e:
            print(e)
            return HttpResponse(status=500)
    return HttpResponse(request.user.pk, status=200)


def tasks_by_tag(request, tag):
    try:
        tag = Tag.objects.get(tag_name=tag)
    except Tag.DoesNotExist as e:
        print(e)
        HttpResponse(status=500)
    tasks = []
    for task in Task.objects.all():
        if tag in task.tags.all():
            tasks.append({'task': task, 'tags': task.tags.all()})
    return render(request, 'task/tasks_by_tag.html', {'tag': tag, 'tasks': tasks})
