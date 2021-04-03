from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('users', views.api_overview),
    path('user/register/', views.RegisterAPI.as_view()),
    # path('', views.apiOverview),
    # path('register/', views.RegisterAPI.as_view(), name='register'),
    # path('login/', views.LoginAPI.as_view(), name='login'),
    # path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall')
    # path('task-delete/', views.taskDelete),
]