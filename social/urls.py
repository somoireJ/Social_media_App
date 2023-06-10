from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('feed/', views.feed , name='feed'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('user/search/', views.user_search, name='user_search'),
    path('notification/', views.notification, name='notification'),
    path('api/users/', views.UserAPIView.as_view(), name='user_api'),
]
