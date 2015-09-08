# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0003_delete_condition'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solving',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('solving_time', models.DateTimeField(auto_now_add=True)),
                ('is_solved', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['solving_time'],
            },
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['creation_date']},
        ),
        migrations.AddField(
            model_name='solving',
            name='task',
            field=models.ForeignKey(to='task.Task'),
        ),
        migrations.AddField(
            model_name='solving',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
