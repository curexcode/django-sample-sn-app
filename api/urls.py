from django.contrib import admin
from django.urls import path, include
from . import views
from knox import views as knox_views


urlpatterns = [
    path('users', views.api_overview),
    path('user/register/', views.RegisterAPI.as_view()),
    # path('user/1/changepassword', views.),
    path('user/login/', views.LoginAPI.as_view()),
    path('user/update-profile/', views.UpdateProfileView.as_view(), name='update-profile'),
    path('user/password-reset/', views.ChangePasswordView.as_view(), name='password-reset'),
    path('user/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('user/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('add-friend/<int:user_id>', views.add_friend, name='add_friend'),
    # path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall')
    # path('', views.apiOverview),
    # path('register/', views.RegisterAPI.as_view(), name='register'),
    # path('login/', views.LoginAPI.as_view(), name='login'),
    # path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall')
    # path('task-delete/', views.taskDelete),
]