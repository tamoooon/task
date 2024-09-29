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
        print(request.POST)  # 送信されたデータを表示してデバッグ
        # カテゴリが空の場合は "test" カテゴリを設定
        # if not request.POST.get('category'):
        #     # "test" カテゴリを取得
        #     test_category = TaskCategory.objects.filter(category_name='test').first()
        #     if test_category:
        #         # フォームのデータを辞書として取得し、カテゴリを追加
        #         form_data = request.POST.copy()
        #         form_data['category'] = test_category.category_id  # 修正: category_id を使用
        #         form = TaskForm(form_data)

        # print(f'form:{form}')
                
        # フォームのエラーメッセージをデバッグ出力
        if not form.is_valid():
            print(form.errors)  # ここでエラー内容を確認

        if form.is_valid():
            print(f'is_valid:{form}')
            task = form.save(commit=False)
            task.user = request.user
            
            # カテゴリを "test" に強制設定
            # test_category = TaskCategory.objects.filter(category_name='test').first()
            # if test_category:
            #     task.category = test_category
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
            print(f'formerror:{context}')
            return render(request, 'task/index.html', context)
    return redirect(to='/task')