from django.urls import path
from posts import views

urlpatterns = [
    path('posts/', views.ShowUserPost.as_view(), name='post'),
    path('posts/<int:pk>', views.ShowOtherPosts.as_view(), name='other_user_posts'),
    path('single_post/<int:pk>', views.ShowSinglePost.as_view(), name='single_post'),
    path('new_post/', views.CreatePost.as_view(), name='new_post'),
    path('like_post/<int:pk>', views.LikePostView.as_view(), name='like_post'),
    path('comment/<int:pk>', views.CommentView.as_view(), name='comment'),
    path('like_comment/<int:pk>', views.LikeCommentView.as_view(), name='like_comment'),
    path('reply_comment/<int:pk>', views.ReplyCommentView.as_view(), name='reply_comment'),
    path('like_reply/<int:pk>', views.LikeReplyView.as_view(), name='like_reply'),
]