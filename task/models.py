from django.contrib.auth.models import User
from django.db import models
from django_markdown.models import MarkdownField


class Tag(models.Model):
    tag_name = models.CharField(max_length=30, unique=True)
    number_of_usages = models.IntegerField(default=0)    # default=1 ???????

    def __str__(self):
        return self.tag_name


class TaskManager(models.Manager):
    def count_tasks_for_user(self, user):
        return len(super(TaskManager, self).filter(user=user))

    def create_task_from_fields(self, task_fields, user):
        task = super(TaskManager, self).create(user=user, task_name=task_fields['task_name'], area=task_fields['area'],
                                               level=task_fields['level'], condition=task_fields['markdown'])
        for tag_name in task_fields['tags']:
            tag = Tag.objects.get_or_create(tag_name=tag_name)[0]
            task.tags.add(tag)
            tag.number_of_usages += 1
            tag.save()
        for answer_text in task_fields['answers']:
            Answer.objects.create(text=answer_text, task=task)
        return task


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

    attempts = models.IntegerField(default=0)
    success_attempts = models.IntegerField(default=0)

    objects = TaskManager()

    class Meta:
        ordering = ['creation_date']

    def __str__(self):
        return self.task_name

    def edit_task_from_fields(self, task_fields):
        self.area = task_fields['area']
        self.level = task_fields['level']
        self.condition = task_fields['markdown']
        self.task_name = task_fields['task_name']
        self.save()
        for tag in self.tags.all():
            self.tags.remove(tag)
            tag.number_of_usages -= 1
            tag.save()
            if tag.number_of_usages < 1:
                tag.delete()
        for tag_text in task_fields['tags']:
            tag = Tag.objects.get_or_create(tag_name=tag_text)[0]
            tag.number_of_usages += 1
            tag.save()
            self.tags.add(tag)
        Answer.objects.filter(task=self).delete()
        for answer_text in task_fields['answers']:
            Answer.objects.create(text=answer_text, task=self)

    def task_statistics(self):
        statistic = {'rating': Rating.objects.average_rating_for_task(self),
                     'percentage': 0 if self.attempts == 0
                     else int(100 * self.success_attempts / self.attempts),
                     'attempts': self.attempts,
                     'task': self}
        return statistic

    def solving_attempt(self, success=False):
        if success:
            self.success_attempts += 1
        self.attempts += 1
        self.save()

    def check_answer(self, answer):
        return Answer.objects.filter(task=self, text=answer).exists()



class Answer(models.Model):
    task = models.ForeignKey(Task, related_name='task_answer')
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.text


class SolvingManager(models.Manager):
    # def count_solves_for_user(self, user):
    #     return len(super(SolvingManager, self).filter(user=user, is_solved=True))
    #
    # def is_first_solving(self, task):
    #     return len(super(SolvingManager, self).filter(task=task)) == 1
    #
    # def percentage_for_task(self, task):
    #     if super(SolvingManager, self).filter(task=task).exists():
    #         return int((len(super(SolvingManager, self).filter(task=task, is_solved=True)) /
    #                     len(super(SolvingManager, self).filter(task=task))) * 100)
    #     else:
    #         return 0
    #
    # def attempts_for_task(self, task):
    #     return len(super(SolvingManager, self).filter(task=task))
    #
    # def percentage_for_user(self, user):
    #     if super(SolvingManager, self).filter(user=user).exists():
    #         return int((len(super(SolvingManager, self).filter(user=user, is_solved=True)) /
    #                     len(super(SolvingManager, self).filter(user=user))) * 100)
    #     else:
    #         return 0

    def rating_for_user(self, user):
        summa = 0
        for solving in super(SolvingManager, self).filter(user=user, is_solved=True):
            summa += solving.level
        return summa

    def attempts_count(self, user, task):
        return len(super(SolvingManager, self).filter(user=user, task=task))

    def solved_tasks_for_user(self, user):
        return [{'task': solving.task, 'tags': solving.task.tags.all(),
                 'count': Solving.objects.attempts_count(user, solving.task)}
                if solving.task else None  # {'task': None, 'tags': None,
                #                       'count': Solving.objects.attempts_count(found_user, solving.task)}
                for solving in super(SolvingManager, self).filter(user=user, is_solved=True)]


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
    def get_mark_or_None(self, user, task):
        return super(RatingManager, self).filter(user=user, task=task).first()

    def average_rating_for_task(self, task):
        ratings = super(RatingManager, self).filter(task=task)
        if ratings.exists():
            return round(sum([x.mark for x in ratings]) / len(ratings), 2)
        else:
            return 0

    def put_rating_from_fields(self, rating_fields):
        user = User.objects.filter(pk=rating_fields['userid']).first()
        task = Task.objects.filter(pk=rating_fields['taskid']).first()
        mark = rating_fields['mark']
        if not self.get_mark_or_None(user, task):
            super(RatingManager, self).create(user=user, task=task, mark=mark)
        return self.average_rating_for_task(task)


class Rating(models.Model):
    user = models.ForeignKey(User)
    task = models.ForeignKey(Task)
    mark = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    objects = RatingManager()

    def __str__(self):
        return '{0.user} put mark {0.mark} for task {0.task}'.format(self)
