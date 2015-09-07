from django.contrib.auth.models import User
from django.db import models
from django_markdown.models import MarkdownField


class Tag(models.Model):
    tag_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.tag_name


class Task(models.Model):
    TASK_LEVEL = ((1, 'Low'), (2, 'Middle'), (3, 'High'),)
    TASK_AREA = ((1, 'Java'), (2, 'C#'), (3, 'Python'), (4, 'Ruby'),)
    user = models.ForeignKey(User, related_name='task_owner')
    task_name = models.CharField(max_length=30)
    tags = models.ManyToManyField(Tag)
    level = models.IntegerField(choices=TASK_LEVEL, default=1)
    area = models.IntegerField(choices=TASK_AREA, default=1)
    condition = MarkdownField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name


class Answer(models.Model):
    task = models.ForeignKey(Task, related_name='task_answer')
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.text
