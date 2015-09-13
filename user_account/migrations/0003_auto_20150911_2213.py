# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0002_achievement_fulldescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='pictureUrl',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
