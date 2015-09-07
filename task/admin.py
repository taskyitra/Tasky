from django.contrib import admin

# Register your models here.
from task.models import Tag, Task, Condition, Answer

# Register your models here.
admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(Condition)
admin.site.register(Answer)
