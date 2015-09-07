# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20150907_2143'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Condition',
        ),
    ]
