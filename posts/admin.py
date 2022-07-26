from django.contrib import admin
from posts.models import Posts, LikePost, Comment, LikeComment, ReplyComment, LikeReply


admin.site.register(Posts)
admin.site.register(LikePost)
admin.site.register(Comment)
admin.site.register(LikeComment)
admin.site.register(ReplyComment)
admin.site.register(LikeReply)
