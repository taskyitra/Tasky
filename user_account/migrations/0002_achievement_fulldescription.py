# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='fullDescription',
            field=models.CharField(default='', max_length=100),
        ),
    ]
