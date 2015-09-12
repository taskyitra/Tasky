from django.contrib.auth.models import User
from django.db import models
from django_markdown.models import MarkdownField


class Tag(models.Model):
    tag_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.tag_name


class TaskManager(models.Manager):
    def count_tasks_for_user(self, user):
        return len(super(TaskManager, self).filter(user=user))


class Task(models.Model):
    TASK_LEVEL = ((1, 'Low'), (2, 'Middle'), (3, 'High'),)
    TASK_AREA = ((1, 'Java'), (2, 'C#'), (3, 'Python'), (4, 'Ruby'),)
    user = models.ForeignKey(User, related_name='task_owner')
    task_name = models.CharField(max_length=30)
    tags = models.ManyToManyField(Tag)
    level = models.IntegerField(choices=TASK_LEVEL, default=1)
    area = models.IntegerField(choices=TASK_AREA, default=1)
    condition = MarkdownField()
    creation_date = models.DateTimeField(auto_now_add=True)
    objects = TaskManager()

    class Meta:
        ordering = ['creation_date']

    def __str__(self):
        return self.task_name


class Answer(models.Model):
    task = models.ForeignKey(Task, related_name='task_answer')
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.text


class SolvingManager(models.Manager):
    def count_solves_for_user(self, user):
        return len(super(SolvingManager, self).filter(user=user, is_solved=True))

    def is_first_solving(self, task):
        return len(super(SolvingManager, self).filter(task=task)) == 1


class Solving(models.Model):
    user = models.ForeignKey(User)
    task = models.ForeignKey(Task, blank=True, null=True, on_delete=models.SET_NULL)
    solving_time = models.DateTimeField(auto_now_add=True)
    is_solved = models.BooleanField(default=False)
    level = models.IntegerField(default=1)
    objects = SolvingManager()

    class Meta:
        ordering = ['solving_time']

    def __str__(self):
        return '{0} {1} task "{2}"' \
            .format(self.user, 'solved' if self.is_solved else 'did not solve', self.task)


class RatingManager(models.Manager):
    def did_he_put_mark(self, user, task):
        return super(RatingManager, self).filter(user=user, task=task).first()

    def average_rating_for_task(self, task):
        ratings = super(RatingManager, self).filter(task=task)
        if ratings.exists():
            return sum([x.mark for x in ratings]) / len(ratings)
        else:
            return 0


class Rating(models.Model):
    user = models.ForeignKey(User)
    task = models.ForeignKey(Task)
    mark = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    objects = RatingManager()

    def __str__(self):
        return '{0.user} put mark {0.mark} for task {0.task}'.format(self)
