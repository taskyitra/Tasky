from django.contrib import admin

# Register your models here.
from task.models import Tag, Task, Answer, Solving
from django_markdown.admin import MarkdownModelAdmin

admin.site.register(Task, MarkdownModelAdmin)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(Solving)
