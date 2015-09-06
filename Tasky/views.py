from django.shortcuts import render
from social.apps.django_app.default.models import UserSocialAuth

__author__ = 'Stanislau'


def index(request):
    ctx = {}  # Возвращаем контекст с данными для начальной страницы
    return render(request, 'base.html', ctx)
