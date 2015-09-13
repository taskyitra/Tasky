# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0007_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_rating',
            field=models.FloatField(default=0),
        ),
    ]
