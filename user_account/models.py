from django.contrib.auth.models import User
from django.db import models
from task.models import Task, Solving


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
    Locals = ((0, 'ru'), (1, 'en'))
    user = models.OneToOneField(User, primary_key=True)
    achievements = models.ManyToManyField(Achievement, through='AchievementsSettings')
    pictureUrl = models.CharField(max_length=100, null=True)
    locale = models.IntegerField(default=0, choices=Locals)

    # rating = models.IntegerField(default=0)
    # attempts = models.IntegerField(default=0)
    # solved_task_count = models.IntegerField(default=0)

    objects = UserProfileManager()

    def statistics(self):
        return {'task_count': Task.objects.count_tasks_for_user(self.user),
                'percentage': Solving.objects.percentage_for_user(self.user),
                'rating': Solving.objects.rating_for_user(self.user),
                'solved_task_count': Solving.objects.count_solves_for_user(self.user)}

    def __str__(self):
        return 'Profile for "{}"'.format(self.user)


class AchievementsSettingsManager(models.Manager):
    def increment_counter(self, profile, achievement):
        achSetting = super(AchievementsSettingsManager, self).get_or_create(userProfile=profile,
                                                                            achievement=achievement)[0]
        achSetting.count = achSetting.count + 1
        achSetting.save()
        return achSetting.count

    def get_achievements_for_user(self, user):
        return [{'achieve': ach.achievement, 'count': ach.count,
                 'its_name_is_first': ach.achievement.name == 'First'} for ach in
                super(AchievementsSettingsManager, self).filter(
                    userProfile=UserProfile.objects.get_or_create_profile(user))]


class AchievementsSettings(models.Model):
    userProfile = models.ForeignKey(UserProfile)
    achievement = models.ForeignKey(Achievement)
    count = models.IntegerField(default=0)
    objects = AchievementsSettingsManager()

    def __str__(self):
        return '{0} has {1} {2}'.format(self.userProfile.user, self.count, self.achievement.description)
