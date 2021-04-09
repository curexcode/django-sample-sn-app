from django.contrib import admin
from django.urls import path, include
from . import views
from knox import views as knox_views


urlpatterns = [
    # Auth related APIs
    path('users', views.api_overview),
    path('user/register/', views.RegisterAPI.as_view()),
    # path('user/1/changepassword', views.),
    path('user/login/', views.LoginAPI.as_view()),
    path('user/update-profile/', views.UpdateProfileView.as_view(), name='update-profile'),
    path('user/password-reset/', views.ChangePasswordView.as_view(), name='password-reset'),
    path('user/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('user/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('user/<int:user_id>/', views.get_profile, name='get_profile'),

    # Friend request related APIs
    path('friends/<int:user_id>', views.get_friends, name='get_friends' ),
    path('pending-requests', views.get_pending_requests, name='get_pending_requests' ),
    path('add-friend/<int:user_id>', views.add_friend, name='add_friend'),
    path('remove-friend/<int:user_id>', views.remove_friend, name='remove_friend' ),
    path('approve-request/<int:user_id>', views.approve_request, name='approve_request' ),
    # Filter can be gender and city param can be either name or phone number
    path('friends/search/<str:gender>/<str:city>/<str:search_str>', views.search_friend , name='search_friend' ),

    # Feed post related APIs.
    path('user/<int:user_id>/feed/', views.get_feed, name='get_feed'),
    path('user/feed/', views.current_user_feed, name='current_user_feed'),
    path('post/<int:id>/comment/', views.NewCommentAPI.as_view(), name='add_new_comment'),
    path('comment/<int:post_id>/', views.get_comments, name='get_comments'),
    path('like-post/<int:post_id>/', views.like_post, name='like_post'),
    path('like-comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('post/newpost/', views.NewPostAPI.as_view(), name='add_new_post'),
    # Here ID = post ID
    # path('post/<int:id>/comment/', views.NewCommentAPI.as_view(), name='add_new_post'),


]


    # path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall')
    # path('', views.apiOverview),
    # path('register/', views.RegisterAPI.as_view(), name='register'),
    # path('login/', views.LoginAPI.as_view(), name='login'),
    # path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall')
    # path('task-delete/', views.taskDelete),