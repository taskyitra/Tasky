from django.contrib.auth import logout
from django.shortcuts import render, render_to_response, redirect

# Create your views here.
from django.template import RequestContext
from account.forms import UserRegistrationForm


def login(request):
    return render(request, 'account/login.html')


def logoutUser(request):
    logout(request)
    return redirect('/')
