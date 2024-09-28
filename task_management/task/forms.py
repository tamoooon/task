from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'detail', 'due_date', 'priority', 'category', 'status', 'start_date']