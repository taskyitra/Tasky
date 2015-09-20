from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from comments.models import Comment
from task.models import Task


class ViewsTest(TestCase):
    fixtures = ['fixtures/dump.json']

    def setUp(self):
        super(ViewsTest, self).setUp()
        login = self.client.login(username='stas', password='stas')

    def test_adding(self):
        resp = self.client.post(reverse('comments:add_comment'),
                                {'pk': Task.objects.first().pk, 'text': 'TEST'})
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(reverse('comments:add_comment'),
                                {'pk': 12345, 'text': 'TEST'})
        self.assertEqual(resp.status_code, 500)
        self.assertEqual(Comment.objects.filter(user=User.objects.get(pk=2)).last().text, 'TEST')
