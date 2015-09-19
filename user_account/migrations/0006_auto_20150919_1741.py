# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0005_userprofile_locale'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='solved_task_count',
            field=models.IntegerField(default=0),
        ),
    ]
