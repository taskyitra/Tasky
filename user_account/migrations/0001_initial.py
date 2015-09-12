# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('imageUrl', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AchievementsSettings',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('count', models.IntegerField(default=1)),
                ('achievement', models.ForeignKey(to='user_account.Achievement')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
                ('pictureUrl', models.CharField(max_length=100)),
                ('achievements', models.ManyToManyField(through='user_account.AchievementsSettings', to='user_account.Achievement')),
            ],
        ),
        migrations.AddField(
            model_name='achievementssettings',
            name='userProfile',
            field=models.ForeignKey(to='user_account.UserProfile'),
        ),
    ]
