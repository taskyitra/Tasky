from django.forms import Form
from django import forms

class TaskSolvingForm(Form):
    answer = forms.CharField(max_length=50, widget=forms.TextInput)