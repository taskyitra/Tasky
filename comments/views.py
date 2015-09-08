import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from comments.models import Comment
from task.models import Task


@login_required
@csrf_protect
def add(request):
    try:
        if request.is_ajax():
            posts_count = request.POST
            d = posts_count.dict()
            json_str = ""
            for i in d.items():
                json_str = i[0]
            json_obj = json.loads(json_str)
            pk = json_obj['pk']
            text = json_obj['text']
            task = Task.objects.filter(pk=pk).first()
            comment = Comment(user=request.user, task=task, text=text)
            comment.save()
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
    return HttpResponse(status=200)
