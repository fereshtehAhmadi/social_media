from rest_framework import serializers
from posts.models import Posts, LikePost, Comment, LikeComment, ReplyComment, LikeReply


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'
