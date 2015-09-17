from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from user_account.models import UserProfile


class UserAccountViewsTest(TestCase):
    fixtures = ['fixtures/dump.json']

    def setUp(self):
        login = self.client.login(username='stas', password='stas')

    def test_base(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_user(self):
        resp = self.client.get('/user_account/user/123/')
        self.assertEqual(resp.status_code, 500)
        resp = self.client.get('/user_account/user/2/')
        self.assertEqual(resp.status_code, 200)

    def test_change_locale(self):
        resp = self.client.post('/user_account/change_locale/', {'pk': 1, 'locale': 0})
        self.assertEqual(resp.status_code, 500)
        resp = self.client.post('/user_account/change_locale/', {'pk': 2, 'locale': 0})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(UserProfile.objects.get_or_create_profile(User.objects.get(pk=2)).locale, 0)
        resp = self.client.post('/user_account/change_locale/', {'pk': 2, 'locale': 1})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(UserProfile.objects.get_or_create_profile(User.objects.get(pk=2)).locale, 1)

    def test_change_username(self):
        resp = self.client.post('/user_account/change_username/', {'value': 'stas1'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(User.objects.get(pk=2).username, 'stas1')
        resp = self.client.post('/user_account/change_username/', {'value': 'stas'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(User.objects.get(pk=2).username, 'stas')
        resp = self.client.post('/user_account/change_username/', {'value': 'stas'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(User.objects.get(pk=2).username, 'stas')
        resp = self.client.post('/user_account/change_username/', {'value': 'stanislau'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(User.objects.get(pk=2).username, 'stas')
        resp = self.client.post('/user_account/change_username/', {'values': 'stanislau'})
        self.assertEqual(resp.status_code, 500)
