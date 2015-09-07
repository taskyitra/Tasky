from django.contrib import admin

# Register your models here.
from task.models import Tag, Task, Answer
from django_markdown.admin import MarkdownModelAdmin

admin.site.register(Task, MarkdownModelAdmin)
admin.site.register(Tag)
admin.site.register(Answer)
