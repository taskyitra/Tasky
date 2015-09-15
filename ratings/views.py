from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from task.models import Task, Answer, Solving, Rating, Tag
import math


def task_rating(request):
    tasks = Task.objects.all()
    for task in tasks:
        task.rating = Rating.objects.average_rating_for_task(task)
    return render(request, 'ratings/task_rating.html', {'tasks': tasks})


def user_rating(request):
    users = User.objects.all()
    user_info = {}
    for user in users:
        user_info[user] = user
        user_info[user].solved = 0
        user_info[user].attempts = 0
        user_info[user].accuracy = 0
    solutions = Solving.objects.all()
    for solution in solutions:
        if solution.is_solved:
            user_info[solution.user].solved += 1
        user_info[solution.user].attempts += 1
        user_info[solution.user].accuracy = math.ceil(
            100 * user_info[solution.user].solved / user_info[solution.user].attempts
        )
    return render(request, 'ratings/user_rating.html', {'users': user_info.values()})
