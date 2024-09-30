from django.db import models
from django.contrib.auth.models import User

class TaskCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255, null=False)
    register_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.category_name

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    detail = models.TextField(null=True, blank=True)
    due_date = models.DateField(null=False)
    priority = models.PositiveSmallIntegerField(null=False)
    category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE, null=True)
    register_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    status = models.PositiveSmallIntegerField(default=0, choices=[
        (0, '未着手'),
        (1, '進行中'),
        (2, '保留'),
        (3, '完了')
    ])
    start_date = models.DateField(null=True, blank=True) # 着手日
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # タスクの所有者

    class Meta:
        ordering = ('-status',)
        constraints = [
            models.CheckConstraint(check=models.Q(priority__gte=1, priority__lte=5), name='priority_range')
        ]

    def __str__(self):
        return self.title