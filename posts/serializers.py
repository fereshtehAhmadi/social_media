from rest_framework import serializers
from posts.models import (Posts, Gallery, LikePost, Comment, LikeComment,
                          ReplyComment, LikeReply, BookMarck)


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class CreateGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['id', 'image', ]


class CreatePostSerializer(serializers.ModelSerializer):
    postimage_set = CreateGallerySerializer(many=True)
    class Meta:
        model = Posts
        fields = '__all__'
    
    def create(self, validated_date):
        post = Posts.objects.create(**validated_data)
        image = self.context['request'].FILES.getlist('image')

        for i in list(image):
            m2 = Gallery(post=post, image= i)
            m2.save()


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        feilds = ['content', ]


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CreateReplyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyComment
        fields = ['content', ]


class ReplyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyComment
        fields = '__all__'


class BookMarckSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMarck
        fields = '__all__'


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = ['user']
        depth = 1


class LikeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeComment
        fields = '__all__'
        depth = 1


class LikeReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeReply
        fields = '__all__'
        depth = 1
