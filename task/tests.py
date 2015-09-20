from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from task.models import Task, Answer
from user_account.models import UserProfile, Achievement, AchievementsSettings


class TaskViewsTest(TestCase):
    fixtures = ['fixtures/dump.json']

    def setUp(self):
        super(TaskViewsTest, self).setUp()
        self.client.login(username='stas', password='stas')

    def test_task_creating(self):
        resp = self.client.post(reverse('task:create'),
                                {'task': ['{"task_name":"a","tags":["a","pythonYEAH"],"level":3,' +
                                          '"markdown":"abc","area":2,"answers":["c","b","a"]}']})
        self.assertEqual(resp.status_code, 200)
        task = Task.objects.filter(user=User.objects.get(pk=2)).last()
        self.assertEqual(task.task_name, 'a')
        self.assertEqual(len(task.tags.all()), 2)
        self.assertEqual(len(Answer.objects.filter(task=task)), 3)
        self.assertEqual(task.level, 3)
        self.assertEqual(task.area, 2)
        self.assertEqual(task.condition, 'abc')
        self.assertEqual(task.user, User.objects.get(pk=2))

    def test_error_task_creating(self):
        resp = self.client.post(reverse('task:create'),
                                {'task': ['_name":"a","tags":["a","b"],"level":3,' +
                                          '"markdown":"abc","area":2,"answers":["c","b","a"]}']})
        self.assertEqual(resp.status_code, 500)

    def test_task_editing_get(self):
        resp = self.client.post(reverse('task:create'),
                                {'task': ['{"task_name":"a","tags":["a","pythonYEAH"],"level":3,' +
                                          '"markdown":"abc","area":2,"answers":["c","b","a"]}']})
        self.assertEqual(resp.status_code, 200)
        task = Task.objects.filter(user=User.objects.get(pk=2)).last()
        resp = self.client.get(
            reverse('task:edit', kwargs={'pk': task.pk}),
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(('task' and 'answers' and 'tags') in resp.context)
        self.assertEqual(len(resp.context['tags']), 2)
        self.assertEqual(len(resp.context['answers']), 3)

    def test_task_editing_post(self):
        resp = self.client.post(reverse('task:create'),
                                {'task': ['{"task_name":"a","tags":["a","pythonYEAH"],"level":3,' +
                                          '"markdown":"abc","area":2,"answers":["c","b","a"]}']})
        self.assertEqual(resp.status_code, 200)
        task = Task.objects.filter(user=User.objects.get(pk=2)).last()
        resp = self.client.post(
            reverse('task:edit', kwargs={'pk': task.pk}),
            {'task':
                 ['{"task_name":"b","tags":["a","b","pythonYEAH"],"level":3,' +
                  '"markdown":"abc","area":2,"answers":["d","c","b","a"]}']})
        self.assertEqual(resp.status_code, 200)
        task = Task.objects.filter(user=User.objects.get(pk=2)).last()
        self.assertEqual(task.task_name, 'b')
        self.assertEqual(len(task.tags.all()), 3)
        self.assertEqual(len(Answer.objects.filter(task=task)), 4)
        self.assertEqual(task.level, 3)
        self.assertEqual(task.area, 2)
        self.assertEqual(task.condition, 'abc')
        self.assertEqual(task.user, User.objects.get(pk=2))

    def test_task_edit_redirect_to_solve(self):
        self.client.login(username='stanislau', password='ckfdujhjl')
        resp = self.client.get(
            reverse('task:edit', kwargs={'pk': Task.objects.filter(user=User.objects.get(pk=2)).first().pk}),
        )
        self.assertEqual(resp.status_code, 302)
        self.client.login(username='stas', password='stas')

    def test_error_task_editing(self):
        resp = self.client.post(
            reverse('task:edit', kwargs={'pk': Task.objects.filter(user=User.objects.get(pk=2)).first().pk}),
            {'task':
                 ['name":"a","tags":["a","b"],"level":3,"markdown":"abc","area":2,"answers":["c","b","a"]}']})
        self.assertEqual(resp.status_code, 500)

    def test_task_solve_redirect_to_edit(self):
        resp = self.client.get(
            reverse('task:solve_task', kwargs={'pk': Task.objects.filter(user=User.objects.get(pk=2)).first().pk}),
        )
        self.assertEqual(resp.status_code, 200)

    def test_task_solving_get(self):
        self.client.login(username='stanislau', password='ckfdujhjl')
        resp = self.client.get(
            reverse('task:solve_task', kwargs={'pk': Task.objects.filter(user=User.objects.get(pk=2)).last().pk}),
        )
        self.assertEqual(resp.status_code, 200)
        self.client.login(username='stas', password='stas')

    def test_task_solving_post(self):
        resp = self.client.post(reverse('task:create'),
                                {'task': ['{"task_name":"a","tags":["a","pythonYEAH"],"level":3,' +
                                          '"markdown":"abc","area":2,"answers":["c","b","a"]}']})
        self.assertEqual(resp.status_code, 200)
        self.client.login(username='stanislau', password='ckfdujhjl')
        resp = self.client.post(
            reverse('task:solve_task', kwargs={'pk': Task.objects.filter(user=User.objects.get(pk=2)).last().pk}),
            {'text': ['w']}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['form'])
        self.assertTrue("Неправильный ответ" in str(resp.context['form']))
        profile = UserProfile.objects.get_or_create_profile(User.objects.get(pk=1))
        profile.locale = 1
        profile.save()
        resp = self.client.post(
            reverse('task:solve_task', kwargs={'pk': Task.objects.filter(user=User.objects.get(pk=2)).last().pk}),
            {'text': ['w']}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['form'])
        self.assertTrue("Wrong answer" in str(resp.context['form']))
        resp = self.client.post(
            reverse('task:solve_task', kwargs={'pk': Task.objects.filter(user=User.objects.get(pk=2)).last().pk}),
            {'text': ['c']}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['form'])

    def test_put_mark(self):
        resp = self.client.post(reverse('task:put_mark_for_task'),
                                {'data': ['{"userid":2,"taskid":50,"mark":4}']})
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(reverse('task:put_mark_for_task'),
                                {'data': ['erid":2,"taskid":50,"mark":4}']})
        self.assertEqual(resp.status_code, 500)

    def test_set_achieves(self):
        for i in range(1):
            resp = self.client.post(reverse('task:create'),
                                    {'task': ['{"task_name":"a","tags":["a","pythonYEAH"],"level":3,' +
                                              '"markdown":"abc","area":2,"answers":["c","b","a"]}']})
            self.assertEqual(resp.status_code, 200)
        profile = UserProfile.objects.get_or_create_profile(User.objects.get(pk=2))
        cr1 = Achievement.objects.get(name='Creator1')
        self.assertTrue(AchievementsSettings.objects.filter(achievement=cr1, userProfile=profile).exists())
        for i in range(5):
            resp = self.client.post(reverse('task:create'),
                                    {'task': ['{"task_name":"a","tags":["a","pythonYEAH"],"level":3,' +
                                              '"markdown":"abc","area":2,"answers":["c","b","a"]}']})
            self.assertEqual(resp.status_code, 200)
        cr2 = Achievement.objects.get(name='Creator2')
        self.assertTrue(AchievementsSettings.objects.filter(achievement=cr2, userProfile=profile).exists())
        for i in range(10):
            resp = self.client.post(reverse('task:create'),
                                    {'task': ['{"task_name":"a","tags":["a","pythonYEAH"],"level":3,' +
                                              '"markdown":"abc","area":2,"answers":["c","b","a"]}']})
            self.assertEqual(resp.status_code, 200)
        cr3 = Achievement.objects.get(name='Creator3')
        self.assertTrue(AchievementsSettings.objects.filter(achievement=cr3, userProfile=profile).exists())
        for i in range(10):
            resp = self.client.post(reverse('task:create'),
                                    {'task': ['{"task_name":"a","tags":["a","pythonYEAH"],"level":3,' +
                                              '"markdown":"abc","area":2,"answers":["c","b","a"]}']})
            self.assertEqual(resp.status_code, 200)
        cr4 = Achievement.objects.get(name='Creator4')
        self.assertTrue(AchievementsSettings.objects.filter(achievement=cr4, userProfile=profile).exists())
