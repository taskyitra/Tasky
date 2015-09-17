from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse

from user_account.models import UserProfile, Achievement, AchievementsSettings


class AchievementTest(TestCase):
    fixtures = ['fixtures/dump.json']

    def setUp(self):
        super(AchievementTest, self).setUp()
        self.achieves = Achievement.objects.all()

    def test_achieves(self):
        pass


class UserProfileTest(TestCase):
    fixtures = ['fixtures/dump.json']

    def setUp(self):
        super(UserProfileTest, self).setUp()
        self.profiles = UserProfile.objects.all()

    def test_profiles(self):
        profile = self.profiles.get(user=User.objects.get(pk=2))
        self.assertEqual(profile.locale, 1)
        self.assertEqual(str(profile), 'Profile for "stas"')

    def test_create_profile(self):
        profile = self.profiles.get(user=User.objects.get(pk=2))
        profile.delete()
        profile = UserProfile.objects.get_or_create_profile(User.objects.get(pk=2))
        self.assertTrue(profile)


class AchSettingsTest(TestCase):
    fixtures = ['fixtures/dump.json']

    def setUp(self):
        super(AchSettingsTest, self).setUp()
        self.achSettings = AchievementsSettings.objects.all()

    def test_achSettings(self):
        pass


class UserAccountViewsTest(TestCase):
    fixtures = ['fixtures/dump.json']

    def setUp(self):
        super(UserAccountViewsTest, self).setUp()
        login = self.client.login(username='stas', password='stas')

    def test_base(self):
        resp = self.client.get(reverse('homepage'))
        self.assertEqual(resp.status_code, 200)

    def test_user(self):
        resp = self.client.get(reverse('user_account:user', kwargs={'pk': 123}))
        self.assertEqual(resp.status_code, 500)
        resp = self.client.get(reverse('user_account:user', kwargs={'pk': 2}))
        self.assertEqual(resp.status_code, 200)

    def test_change_locale(self):
        resp = self.client.post(reverse('user_account:change_locale'), {'pk': 1, 'locale': 0})
        self.assertEqual(resp.status_code, 500)
        resp = self.client.post(reverse('user_account:change_locale'), {'pk': 2, 'locale': 0})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(UserProfile.objects.get_or_create_profile(User.objects.get(pk=2)).locale, 0)
        resp = self.client.post(reverse('user_account:change_locale'), {'pk': 2, 'locale': 1})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(UserProfile.objects.get_or_create_profile(User.objects.get(pk=2)).locale, 1)

    def test_change_username(self):
        resp = self.client.post(reverse('user_account:change_username'), {'value': 'stas1'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(User.objects.get(pk=2).username, 'stas1')
        resp = self.client.post(reverse('user_account:change_username'), {'value': 'stas'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(User.objects.get(pk=2).username, 'stas')
        resp = self.client.post(reverse('user_account:change_username'), {'value': 'stas'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(User.objects.get(pk=2).username, 'stas')
        resp = self.client.post(reverse('user_account:change_username'), {'value': 'stanislau'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(User.objects.get(pk=2).username, 'stas')
        resp = self.client.post(reverse('user_account:change_username'), {'values': 'stanislau'})
        self.assertEqual(resp.status_code, 500)
