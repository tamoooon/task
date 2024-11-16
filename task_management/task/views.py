from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task, TaskCategory
from .forms import TaskForm

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import SignUpForm

# ログイン系
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect(to='/task/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


# 機能系
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    progress = {
        'total': tasks.count(),
        'completed': tasks.filter(status=2).count(),
    }
    categories = TaskCategory.objects.all()

    sort_by = request.GET.get('sort_by', 'status')
    if sort_by == 'due_date':
        tasks = tasks.order_by('due_date')
    elif sort_by == 'priority':
        tasks = tasks.order_by('priority')
    elif sort_by == 'category':
        tasks = tasks.order_by('category')

    context = {
        'tasks': tasks,
        'progress': progress,
        'categories': categories,
        'sort_by': sort_by,
        'form': TaskForm()  # モーダルで使用するフォームをコンテキストに追加
    }
    return render(request, 'task/index.html', context)

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        print(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user

            task.save()
            return redirect(to='/task/')
        else:
            # フォームエラーがある場合は、そのままタスクリストを再表示
            tasks = Task.objects.filter(user=request.user)
            progress = {
                'total': tasks.count(),
                'completed': tasks.filter(status=2).count(),
            }
            categories = TaskCategory.objects.all()
            sort_by = request.GET.get('sort_by', 'status')
            context = {
                'tasks': tasks,
                'progress': progress,
                'categories': categories,
                'sort_by': sort_by,
                'form': form,  # エラーを含むフォームを再表示
            }
            print(f'formerror:{context}')
            return render(request, 'task/index.html', context)
    return redirect(to='/task/')

@login_required
def task_edit(request, task_id):
    task = Task.objects.filter(user=request.user).filter(task_id=task_id).first()
    if not task:
        return redirect(to='/task/')

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(to='/task/')
    else:
        form = TaskForm(instance=task)

    return render(request, 'task/update.html', {'form': form, 'task': task})

@login_required
def task_delete(request, task_id):
    task = Task.objects.filter(user=request.user).filter(task_id=task_id).first()
    if task:
        task.delete()
    return redirect(to='/task/')