from django.urls import path
from posts import views

urlpatterns = [
    path('posts/', views.ShowUserPost.as_view(), name='post'),
    path('posts/<int:pk>', views.ShowOtherPosts.as_view(), name='other_user_posts'),
]