from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task, TaskCategory
from .forms import TaskForm

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

def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect(to='/task')
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
            return render(request, 'task/index.html', context)
    return redirect(to='/task')