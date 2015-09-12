from django.contrib.auth.models import User
from django.db import models
from task.models import Task


class CommentManager(models.Manager):
    def count_comments_for_user(self, user):
        return len(super(CommentManager, self).filter(user=user))


class Comment(models.Model):
    user = models.ForeignKey(User)
    task = models.ForeignKey(Task)
    text = models.CharField(max_length=100)
    creation_time = models.DateTimeField(auto_now_add=True)
    objects = CommentManager()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['creation_time']
