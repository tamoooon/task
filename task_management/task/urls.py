from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('login/', auth_views.LoginView.as_view(template_name='task/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]