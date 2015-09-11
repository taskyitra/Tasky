from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render


@login_required
def change_username(request):
    try:
        new_username = request.POST['value']
        if request.user.username == new_username:
            return HttpResponse(request.POST['value'], status=200)
        if User.objects.filter(username=new_username).exists():
            new_username = request.user.username
        else:
            current_user = request.user
            current_user.username = new_username
            current_user.save()
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
    return HttpResponse(new_username, status=200)


@login_required
def generate_picture(request):
    try:
        pass
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
    return HttpResponse(status=200)


@login_required
def user(request, pk):
    try:
        found_user = User.objects.get(pk=pk)
        pass
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
    return render(request, 'user_account/user.html', {'founduser': found_user})
