from django import forms
from .models import Task
from .models import TaskCategory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'detail', 'due_date', 'priority', 'category', 'status', 'start_date']

class TaskCategoryForm(forms.ModelForm):
    class Meta:
        model = TaskCategory
        fields = ['category_id', 'category_id']