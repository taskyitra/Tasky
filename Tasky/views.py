from django.shortcuts import render
from social.apps.django_app.default.models import UserSocialAuth

__author__ = 'Stanislau'


def index(request):
    # if request.user.is_authenticated():
    #     changeName(request)
    ctx = {}  # Возвращаем контекст с данными для начальной страницы
    return render(request, 'base.html', ctx)


def changeName(request):
    username = request.user.username
    if not (username.startswith('vk:') or username.startswith('github:') or
                username.startswith('fb:') or username.startswith('twitter:')):
        provider = ''
        for user in UserSocialAuth.objects.all():
            if user.user == request.user:
                provider = user.provider
                break
        if provider.startswith('vk'):
            provider = 'vk'
        username = provider + ':' + username
        user = request.user
        user.username = username
        user.save()
