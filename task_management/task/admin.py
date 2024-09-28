from django.contrib import admin
from .models import TaskCategory
from .models import Task

admin.site.register(TaskCategory)
admin.site.register(Task)

