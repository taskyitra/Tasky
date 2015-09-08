from django.contrib.auth.models import User
from django.db import models
from task.models import Task


class Comment(models.Model):
    user = models.ForeignKey(User)
    task = models.ForeignKey(Task)
    text = models.CharField(max_length=100)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['creation_time']
