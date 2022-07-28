from rest_framework import serializers
from posts.models import Posts, Gallery, LikePost, Comment, LikeComment, ReplyComment, LikeReply


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'
    
    def create(self, validated_data):
        post = Posts.objects.create(**validated_data)
        
        gallery = Gallery.objects.create(post = post, **validated_data, )


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', ]


class ReplyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyComment
        fields = ['content', ]
