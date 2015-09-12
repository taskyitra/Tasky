from django.contrib.auth.models import User
from django.db import models


class AchievementManager(models.Manager):
    pass


class Achievement(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    fullDescription = models.CharField(max_length=100, default="")
    imageUrl = models.CharField(max_length=100)
    objects = AchievementManager()

    def __str__(self):
        return self.name


class UserProfileManager(models.Manager):
    def get_or_create_profile(self, user):
        found_user = super(UserProfileManager, self).filter(user=user)
        if found_user.exists():
            return found_user.first()
        else:
            profile = UserProfile(user=user)
            profile.save()
            return profile


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    achievements = models.ManyToManyField(Achievement, through='AchievementsSettings')
    pictureUrl = models.CharField(max_length=100, null=True)
    objects = UserProfileManager()

    def __str__(self):
        return 'Profile for "{}"'.format(self.user)



class AchievementsSettingsManager(models.Manager):
    pass


class AchievementsSettings(models.Model):
    userProfile = models.ForeignKey(UserProfile)
    achievement = models.ForeignKey(Achievement)
    count = models.IntegerField(default=1)
    objects = AchievementsSettingsManager()

    def __str__(self):
        return '{0} has {1} {2}'.format(self.userProfile.user, self.count, self.achievement.description)
