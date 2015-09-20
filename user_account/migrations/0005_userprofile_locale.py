# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0004_auto_20150912_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='locale',
            field=models.IntegerField(default=0, choices=[(0, 'ru'), (1, 'en')]),
        ),
    ]
