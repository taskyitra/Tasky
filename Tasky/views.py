from django.shortcuts import render

__author__ = 'Stanislau'

def index(request):
    ctx = {}  # Возвращаем контекст с данными для начальной страницы
    return render(request, 'base.html', ctx)
