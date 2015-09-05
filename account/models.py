from django.contrib.auth.models import User
from django.db import models

from Tasky import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    hash = models.CharField(max_length=100)

    def __unicode__(self):
        return self.user.username
