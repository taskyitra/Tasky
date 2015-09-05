from django.contrib.auth import logout
from django.shortcuts import render, render_to_response, redirect

# Create your views here.
from django.template import RequestContext
from account.forms import UserRegistrationForm


def login(request):
    return render(request, 'account/login.html')


def signin(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserRegistrationForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.is_active = False
            print("Send Email")
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserRegistrationForm()
    return render_to_response(
        'account/signin.html',
        {'user_form': user_form, 'registered': registered}, context)


def logoutUser(request):
    logout(request)
    return redirect('/')
