from django.forms import ModelForm, Form
from django import forms
from task.models import Task


class CreateTaskForm(Form):
    task_name = forms.CharField(max_length=30, widget=forms.TextInput)
    level = forms.Select(choices=Task.TASK_LEVEL)
    condition = forms.Textarea()
    area = forms.Select(choices=Task.TASK_AREA)

