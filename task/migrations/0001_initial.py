# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('tag_name', models.CharField(unique=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('task_name', models.CharField(max_length=30)),
                ('level', models.IntegerField(default=1, choices=[(1, 'Low'), (2, 'Middle'), (3, 'High')])),
                ('area', models.IntegerField(default=1, choices=[(1, 'Java'), (2, 'C#'), (3, 'Python'), (4, 'Ruby')])),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('condition', models.OneToOneField(to='task.Condition', related_name='task_condition')),
                ('tags', models.ManyToManyField(to='task.Tag')),
                ('user', models.ForeignKey(related_name='task_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='task',
            field=models.ForeignKey(related_name='task_answer', to='task.Task'),
        ),
    ]
