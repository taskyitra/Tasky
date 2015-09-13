import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from comments.models import Comment
from task.models import Task, Solving
from user_account.models import UserProfile, Achievement, AchievementsSettings


def set_achievements_at_commenting(user):
    achivements_names = {5: 'Commentator1', 10: 'Commentator2'}
    count = Comment.objects.count_comments_for_user(user)
    if count in achivements_names.keys():
        profile = UserProfile.objects.get_or_create_profile(user)
        achievement = Achievement.objects.get(name=achivements_names[count])
        if not AchievementsSettings.objects.filter(userProfile=profile, achievement=achievement).exists():
            achSetting = AchievementsSettings(userProfile=profile, achievement=achievement, count=1)
            achSetting.save()


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
            set_achievements_at_commenting(request.user)
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
    return HttpResponse(status=200)
