from django.contrib import admin
from user_account.models import UserProfile, Achievement, AchievementsSettings

admin.site.register(UserProfile)
admin.site.register(Achievement)
admin.site.register(AchievementsSettings)
