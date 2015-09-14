import json
import os
from io import BytesIO
import base64

from PIL import Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.forms.forms import NON_FIELD_ERRORS
import cloudinary
from cloudinary.uploader import upload
from Tasky import settings

from comments.models import Comment
from task.forms import AnswerForm
from task.models import Task, Answer, Solving, Rating, Tag
from user_account.models import UserProfile, Achievement, AchievementsSettings

cloudinary.config(
    cloud_name="dmt04dtgy",
    api_key="326982618723938",
    api_secret="fyssIAtgJ7g-LL1SsqjnLYSQgdc"
)


class TaskStatistic(object):
    def __init__(self, rating, percentage, attempts):
        self.percentage = percentage
        self.rating = rating
        self.attempts = attempts


def set_achievements_at_creation(user):
    achivements_names = {5: 'Creator1', 10: 'Creator2', 20: 'Creator3', 30: 'Creator4'}
    count = Task.objects.count_tasks_for_user(user)
    print(count)
    if count in achivements_names.keys():
        profile = UserProfile.objects.get_or_create_profile(user)
        achievement = Achievement.objects.get(name=achivements_names[count])
        if not AchievementsSettings.objects.filter(userProfile=profile, achievement=achievement).exists():
            achSetting = AchievementsSettings(userProfile=profile, achievement=achievement, count=1)
            achSetting.save()


def set_achievements_at_decision(user, task):
    achivements_names = {5: 'Solver1', 10: 'Solver2', 20: 'Solver3', 30: 'Solver4'}
    count = Solving.objects.count_solves_for_user(user)
    if count in achivements_names.keys():
        profile = UserProfile.objects.get_or_create_profile(user)
        achievement = Achievement.objects.get(name=achivements_names[count])
        if not AchievementsSettings.objects.filter(userProfile=profile, achievement=achievement).exists():
            achSetting = AchievementsSettings(userProfile=profile, achievement=achievement, count=1)
            achSetting.save()
    if Solving.objects.is_first_solving(task):
        profile = UserProfile.objects.get_or_create_profile(user)
        achievement = Achievement.objects.get(name='First')
        AchievementsSettings.objects.increment_counter(profile, achievement)


@login_required
def create_task(request):
    try:
        if request.is_ajax():
            posts_count = request.POST
            d = posts_count.dict()
            json_str = ""
            for i in d.items():
                json_str = i[0]
            json_obj = json.loads(json_str)
            area = json_obj['area']
            level = json_obj['level']
            markdown = json_obj['markdown']
            tags = json_obj['tags']
            answers = json_obj['answers']
            task_name = json_obj['task_name']
            task = Task(user=request.user, task_name=task_name, area=area, level=level,
                        condition=markdown)
            task.save()
            for tag_text in tags:
                tag = Tag.objects.filter(tag_name=tag_text).first()
                if tag is None:
                    tag = Tag(tag_name=tag_text)
                    tag.save()
                task.tags.add(tag)
            for answer_text in answers:
                answer = Answer(text=answer_text, task=task)
                answer.save()
            set_achievements_at_creation(request.user)
            return HttpResponse(task.pk, status=200)
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
    return render(request, 'task/create_task.html')


@login_required
def edit(request, pk):
    task = Task.objects.filter(pk=pk).first()
    if task.user != request.user:
        return solve_task(request, pk)
    answers = Answer.objects.filter(task=task)
    answers = [{'val': x.text, 'num': i} for i, x in enumerate(answers)]
    tags = task.tags.all()
    tags = [{'val': x.tag_name, 'num': i} for i, x in enumerate(tags)]
    try:
        if request.is_ajax():
            posts_count = request.POST
            d = posts_count.dict()
            json_str = ""
            for i in d.items():
                json_str = i[0]
            json_obj = json.loads(json_str)
            task.area = json_obj['area']
            task.level = json_obj['level']
            task.condition = json_obj['markdown']
            tags = json_obj['tags']
            answers = json_obj['answers']
            task.task_name = json_obj['task_name']
            task.save()
            for tag in task.tags.all():
                task.tags.remove(tag)
            for tag_text in tags:
                tag = Tag.objects.filter(tag_name=tag_text).first()
                if tag is None:
                    tag = Tag(tag_name=tag_text)
                    tag.save()
                task.tags.add(tag)
            Answer.objects.filter(task=task).delete()
            for answer_text in answers:
                answer = Answer(text=answer_text, task=task)
                answer.save()
            return HttpResponse(status=200)
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
    return render(request, 'task/edit.html', {'task': task, 'answers': answers, 'tags': tags})


@login_required
def my_tasks(request):
    user_tasks = Task.objects.filter(user=request.user)
    return render(request, 'task/my_tasks.html', {'tasks': user_tasks})


def task_statistics(task):
    statistic = TaskStatistic(Rating.objects.average_rating_for_task(task),
                              Solving.objects.percentage_for_task(task),
                              Solving.objects.attempts_for_task(task))
    return statistic


@login_required
def solve_task(request, pk):
    task = Task.objects.filter(pk=pk).first()
    if task.user == request.user:
        return edit(request, pk)
    func = lambda x: x if x is not None else '/static/user_account/pictures/unknown.png'
    comments = [{'comment': comment, 'url': func(UserProfile.objects.get_or_create_profile(comment.user).pictureUrl)} for
                comment in Comment.objects.filter(task=task)]
    did_he_put_mark = Rating.objects.did_he_put_mark(request.user, task)
    is_old_solving = Solving.objects.filter(task=task, user=request.user, is_solved=True).exists()
    if is_old_solving:
        return render(request, 'task/solve.html', {'form': None, 'task': task,
                                                   'is_old_solving': is_old_solving,
                                                   'comments': comments,
                                                   'user_mark_for_task': did_he_put_mark,
                                                   'tags': task.tags.all(),
                                                   'statistics': task_statistics(task)})
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
                    set_achievements_at_decision(request.user, task)
                    return render(request, 'task/solve.html', {'form': None, 'task': task, 'is_old_solving': False,
                                                               'comments': comments,
                                                               'user_mark_for_task': did_he_put_mark,
                                                               'tags': task.tags.all(),
                                                               'statistics': task_statistics(task)})
            except Exception as e:
                print(e)
    else:
        form = AnswerForm
    return render(request, 'task/solve.html', {'form': form, 'task': task,
                                               'comments': comments,
                                               'did_user_put': did_he_put_mark,
                                               'tags': task.tags.all(),
                                               'statistics': task_statistics(task)})


@login_required
def put_mark_for_task(request):
    average_rating = 0
    try:
        if request.is_ajax():
            posts_count = request.POST
            d = posts_count.dict()
            json_str = ""
            for i in d.items():
                json_str = i[0]
            json_obj = json.loads(json_str)
            user = User.objects.filter(pk=json_obj['userid']).first()
            task = Task.objects.filter(pk=json_obj['taskid']).first()
            mark = json_obj['mark']
            rating = Rating(user=user, task=task, mark=mark)
            rating.save()
            average_rating = Rating.objects.average_rating_for_task(task)
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
    return HttpResponse(average_rating, status=200)


@login_required
def create_task_success(request, pk):
    return render(request, 'task/create_task_success.html', {'task': Task.objects.filter(pk=pk).first()})


def getOptionsTypeahead(request, query):
    data = []
    try:
        for tag in Tag.objects.all():
            if query in tag.tag_name:
                data.append({'value': tag.tag_name})
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
    return JsonResponse(data, safe=False, status=200)


def add_picture(request):
    try:
        if request.is_ajax():
            posts_count = request.POST
            d = posts_count.dict()
            json_str = ""
            for i in d.items():
                json_str = i[0]
            json_str = json_str.split(',')[1]

            image = Image.open(BytesIO(base64.b64decode(json_str)))
            path = 'user_account/static/user_account/pictures/other/im.png'
            image.save(path, "PNG")
            file = upload(path)
            imageUrl = file['url']
            os.remove(path)

            return HttpResponse(imageUrl, status=200)

    except Exception as e:
        print(e)
        return HttpResponse(status=500)
    return HttpResponse(status=200)
