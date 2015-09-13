from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from task.models import Task, Answer, Solving, Rating, Tag


class TaskInfo(object):
    def __init__(self, task, rating):
        self.task = task
        self.rating = rating


class UserInfo(object):
    def __init__(self, user, rating):
        self.user = user
        self.rating = rating

def task_rating(request):
    tasks = Task.objects.all()
    tasks = (TaskInfo(task, Rating.objects.average_rating_for_task(task)) for task in tasks)
    tasks = sorted(tasks, key=lambda task: task.rating, reverse=True)
    #   user_tasks = sorted(user_tasks, key=user_tasks[1], reverse=True)
    #  return render(request, '')
    return render(request, 'ratings/task_rating.html', {'tasks': tasks})


def user_rating(request):
    right_solutions = Solving.objects.filter(is_solved=True)
    rating_dict = {}
    for solution in right_solutions:
        rating_dict[solution.user] = rating_dict.get(solution.user, 0) + solution.level
    users = (UserInfo(user, rating_dict[user]) for user in rating_dict)
    users = sorted(users, key=lambda user: user.rating, reverse=True)
    return render(request, 'ratings/user_rating.html', {'users': users})
