# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0009_remove_task_task_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='success_attempts',
            field=models.IntegerField(default=0),
        ),
    ]
