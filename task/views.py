import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.forms.forms import NON_FIELD_ERRORS
from comments.models import Comment

from task.forms import CreateTaskForm, AnswerForm
from task.models import Task, Answer, Solving, Rating, Tag


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
            return HttpResponse(task.pk, status=200)
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
    return render(request, 'task/create_task.html')


@login_required
def edit(request, pk):
    task = Task.objects.filter(pk=pk).first()
    if task.user != request.user:
        return HttpResponse("Ошибка доступа")
    answers = Answer.objects.filter(task=task)
    answers = [{'val': x.text, 'num': i} for i, x in enumerate(answers)]
    print(answers)
    tags = task.tags.all()
    tags = [{'val': x.tag_name, 'num': i} for i, x in enumerate(tags)]
    print(tags)
    try:
        if request.is_ajax():
            posts_count = request.POST
            d = posts_count.dict()
            json_str = ""
            for i in d.items():
                json_str = i[0]
            json_obj = json.loads(json_str)
            print(json_obj)
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

    # task = Task.objects.filter(pk=pk).first()
    # answer = Answer.objects.filter(task=task).first()  # Здесь должны быть все
    # if request.method == 'POST':
    #     form = CreateTaskForm(request.POST)
    #     answer_form = AnswerForm(request.POST)
    #     if form.is_valid() and answer_form.is_valid():
    #         try:
    #             task = form.save(commit=False)
    #             task.user = request.user
    #             task.pk = pk
    #             task.creation_date = Task.objects.filter(pk=pk).first().creation_date
    #             task.save()
    #             Answer.objects.filter(task=task).delete()
    #             answer = answer_form.save(commit=False)
    #             answer.task = task
    #             answer.save()
    #         except Exception as e:
    #             print(e)
    # else:
    #     form = CreateTaskForm(instance=task)
    #     answer_form = AnswerForm(instance=answer)
    # return render(request, 'task/edit.html', {'form': form, 'answer_form': answer_form})


@login_required
def my_tasks(request):
    user_tasks = Task.objects.filter(user=request.user)
    return render(request, 'task/my_tasks.html', {'tasks': user_tasks})


@login_required
def solve_task(request, pk):
    task = Task.objects.filter(pk=pk).first()
    comments = Comment.objects.filter(task=task)
    did_he_put_mark = Rating.objects.did_he_put_mark(request.user, task)
    is_old_solving = True if len(Solving.objects.filter(task=task).filter(user=request.user) \
                                 .filter(is_solved=True)) > 0 else False
    if is_old_solving:
        return render(request, 'task/solve.html', {'form': None, 'task': task,
                                                   'is_old_solving': is_old_solving,
                                                   'comments': comments,
                                                   'user_mark_for_task': did_he_put_mark})
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
                                                               'comments': comments,
                                                               'user_mark_for_task': did_he_put_mark})
            except Exception as e:
                print(e)
    else:
        form = AnswerForm
    return render(request, 'task/solve.html', {'form': form, 'task': task,
                                               'comments': comments,
                                               'did_user_put': did_he_put_mark})


@login_required
def put_mark_for_task(request):
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
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
    return HttpResponse(status=200)


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
    print(data)
    return JsonResponse(data, safe=False, status=200)
