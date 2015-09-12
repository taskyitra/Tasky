# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0003_auto_20150911_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievementssettings',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
