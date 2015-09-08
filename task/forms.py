from django.forms import ModelForm
from task.models import Task, Answer


class CreateTaskForm(ModelForm):
    class Meta:
        model = Task
        exclude = ['user']


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        exclude = ['task']


    # task_name = forms.CharField(max_length=30, widget=forms.TextInput)
    # tags = forms.CharField(max_length=30, widget=forms.TextInput)
    # level = forms.IntegerField(widget=forms.Select(choices=Task.TASK_LEVEL))
    # condition = forms.CharField(widget=MarkdownWidget())
    # area = forms.IntegerField(widget=forms.Select(choices=Task.TASK_AREA))
    # answers = forms.CharField(max_length=30, widget=forms.TextInput)

