from django import forms
from django.contrib.auth.models import User

__author__ = 'Stanislau'

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
