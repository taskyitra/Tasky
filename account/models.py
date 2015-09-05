from django.db import models

# Create your models here.
from Tasky import settings


class preRegistration(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
