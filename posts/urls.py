from django.urls import path
from posts import views

urlpatterns = [
    path('posts/', views.ShowUserPost.as_view(), name='post'),
    path('posts/<int:pk>', views.ShowOtherPosts.as_view(), name='other_user_posts'),
    path('single_post/<int:pk>', views.ShowSinglePost.as_view(), name='single_post'),
    path('new_post/', views.CreatePost.as_view(), name='new_post'),
    path('update_post/<int:pk>', views.UpdatePost.as_view(), name='update_post'),
    path('delete_post/<int:pk>', views.DeletePost.as_view(), name='delete_post'),
    
    path('comment/<int:pk>', views.CommentView.as_view(), name='comment'),
    path('delete_comment/<int:pk>', views.DeleteComment.as_view(), name='delete_comment'),
    path('reply_comment/<int:pk>', views.ReplyCommentView.as_view(), name='reply_comment'),
    path('delete_reply_comment/<int:pk>', views.DeleteReplyComment.as_view(), name='delete_reply_comment'),

    path('like_post/<int:pk>', views.LikePostView.as_view(), name='like_post'),
    path('like_comment/<int:pk>', views.LikeCommentView.as_view(), name='like_comment'),
    path('like_reply/<int:pk>', views.LikeReplyView.as_view(), name='like_reply'),
    
    path('show_comments/<int:pk>', views.ShowComment.as_view(), name='show_comments'),
    path('show_reply/<int:pk>', views.ShowReplyComment.as_view(), name='show_reply'),
    
    path('bookmarck/<int:pk>', views.BookMarckView.as_view(), name='bookmarck'),
    path('show_bookmarck/<int:pk>', views.AllBookMarckView.as_view(), name='show_bookmarck'),
]