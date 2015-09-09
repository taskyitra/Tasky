# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_auto_20150908_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solving',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, null=True, to='task.Task'),
        ),
    ]
