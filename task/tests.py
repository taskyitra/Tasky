from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from task.models import Task


class TaskViewsTest(TestCase):
    fixtures = ['fixtures/dump.json']

    def setUp(self):
        super(TaskViewsTest, self).setUp()
        self.client.login(username='stas', password='stas')

    def test_task_creating(self):
        resp = self.client.post(reverse('task:create'),
                                {'task': ['{"task_name":"a","tags":["a","b"],"level":3,' +
                                          '"markdown":"abc","area":2,"answers":["c","b","a"]}']})
        self.assertEqual(resp.status_code, 200)

    def test_error_task_creating(self):
        resp = self.client.post(reverse('task:create'),
                                {'task': ['_name":"a","tags":["a","b"],"level":3,' +
                                          '"markdown":"abc","area":2,"answers":["c","b","a"]}']})
        self.assertEqual(resp.status_code, 500)

    def test_task_editing(self):
        resp = self.client.get(
            reverse('task:edit', kwargs={'pk': Task.objects.filter(user=User.objects.get(pk=2)).first().pk}),
        )
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(
            reverse('task:edit', kwargs={'pk': Task.objects.filter(user=User.objects.get(pk=2)).first().pk}),
            {'task':
                 ['{"task_name":"a","tags":["a","b"],"level":3,"markdown":"abc","area":2,"answers":["c","b","a"]}']})
        self.assertEqual(resp.status_code, 200)

    def test_error_task_editing(self):
        resp = self.client.post(
            reverse('task:edit', kwargs={'pk': Task.objects.filter(user=User.objects.get(pk=2)).first().pk}),
            {'task':
                 ['name":"a","tags":["a","b"],"level":3,"markdown":"abc","area":2,"answers":["c","b","a"]}']})
        self.assertEqual(resp.status_code, 500)

    def test_task_solving(self):
        resp = self.client.get(
            reverse('task:solve_task', kwargs={'pk': Task.objects.filter(user=User.objects.get(pk=2)).first().pk}),
        )
        self.assertEqual(resp.status_code, 200)

        self.client.login(username='stanislau', password='ckfdujhjl')
        resp = self.client.get(
            reverse('task:solve_task', kwargs={'pk': Task.objects.filter(user=User.objects.get(pk=2)).last().pk}),
        )
        self.assertEqual(resp.status_code, 200)
        self.client.login(username='stas', password='stas')

    def test_put_mark(self):
        resp = self.client.post(reverse('task:put_mark_for_task'),
                                {'data': ['{"userid":2,"taskid":50,"mark":4}']})
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(reverse('task:put_mark_for_task'),
                                {'data': ['erid":2,"taskid":50,"mark":4}']})
        self.assertEqual(resp.status_code, 500)
