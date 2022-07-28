from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status, generics, views, permissions
from rest_framework.response import Response

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Count

from accounts.models import Profile
from posts.models import (Posts, Gallery, LikePost, Comment, LikeComment,
                          ReplyComment, LikeReply, BookMarck)
from accounts.renders import UserRender
from posts.serializers import (PostsSerializer, GallerySerializer, CreatePostSerializer,
                               CreateCommentSerializer, ReplyCommentSerializer, BookMarckSerializer,
                               CommentSerializer, CreateReplyCommentSerializer)


class ShowUserPost(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        gallery = Gallery.objects.filter(post__user__username=str(request.user))
        serializer_gallery = GallerySerializer(gallery, many=True)
        content = {
            'gallery': serializer_gallery.data,
        }
        return Response(content, status=status.HTTP_200_OK)


class ShowOtherPosts(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        user = Profile.objects.get(id=pk)
        requester = User.objects.get(username=str(request.user))
        validation = Profile.objects.filter(id=pk, follower=requester).exists()
        if validation:
            post = Posts.objects.get(user__username=user)
            serializer_post = PostsSerializer(post)
            gallery = Gallery.objects.filter(post=post).first()
            serializer_gallery = GallerySerializer(gallery)
            
            content = {
            'post': serializer_post.data,
            'gallery': serializer_gallery.data,
            }   
            return Response(content, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'you cant see this page...'}, status=status.HTTP_400_BAD_REQUEST)


class ShowSinglePost(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        post = Posts.objects.get(id=pk)
        requester = User.objects.get(username=str(request.user))
        validation = Profile.objects.filter(user=post.user, follower=requester).exists()
        if validation or post.user == requester:
            post = Posts.objects.get(id=pk)
            post.views = int(post.views) + 1
            post.save()
            serializer_post = PostsSerializer(post)
            gallery = Gallery.objects.filter(post=post).first()
            serializer_gallery = GallerySerializer(gallery)
            
            like = LikePost.objects.filter(post=post).count()
            comment = Comment.objects.filter(post=post).count()
            content = {
            'post': serializer_post.data,
            'gallery': serializer_gallery.data,
            'like': like,
            'comment': comment,
            }
            
            return Response(content, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'you cant see this post...'}, status=status.HTTP_400_BAD_REQUEST)        


# class CreatePost(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request, format=None):
#         post_serializer = PostsSerializer(data=request.data)
#         if post_serializer.is_valid(raise_exception=True):
#             post = Post.objects.create(post_serializer.data)
#             gallery_serializer = GallerySerializer(data=request.data, many=True)
#             if gallery_serializer.is_valid(raise_exception=True):
#                 gallery = Gallery.objects.create(post=post, image= request.data.get('image'))
                
#                 content = {
#                     'post': post,
#                     'gallery': gallery,
#                 }
#                 return Response(content, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'msg': ':(((((((((((('}, status=status.HTTP_400_BAD_REQUEST)


class CreatePost(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = CreatePostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg':'affarin...'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class LikePostView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        user = User.objects.get(username=str(request.user))
        post = Posts.objects.get(id=pk)
        validation = LikePost.objects.filter(user=user, post=post).exists()
        if validation:
                like = LikePost.objects.get(user=user, post=post)
                like.delete()
        else:
            like = LikePost.objects.get(user=user, post=post)
            like.like = True
            like.save()
        return Response({'msg': 'liked...'}, status=status.HTTP_201_CREATED)


class CommentView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        user = User.objects.get(username=str(request.user))
        post = Posts.objects.get(id=pk)
        serializer = CreateCommentSerializer(data=request.data)
        Comment.objects.create(user=user, post=post, content=request.data.get('content'))
        return Response({'msg': 'send comment...'}, status=status.HTTP_201_CREATED)


class LikeCommentView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        user = User.objects.get(username=str(request.user))
        comment = Comment.objects.get(id=pk)
        validation = LikePost.objects.filter(user=user, comment=comment).exists()
        if validation:
                like = LikeComment.objects.get(user=user, comment=comment)
                like.delete()
        else:
            like = LikeComment.objects.get(user=user, comment=comment)
            like.like = True
            like.save()
        return Response({'msg': 'liked...'}, status=status.HTTP_201_CREATED)


class ShowComment(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        post = Post.objects.get(id=pk)
        comment = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comment, many=True)
        like = LikeComment.objects.filter(comment=comment).count()
        content = {
            'comment': serializer.data,
            'like': like,
        }
        return Response(content, status=status.HTTP_200_OK)


class ReplyCommentView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        user = User.objects.get(username=str(request.user))
        comment = Comment.objects.get(id=pk)
        serializer = CreateReplyCommentSerializer(data=request.data)
        ReplyComment.objects.create(user=user, comment=comment, content=request.data.get('content'))
        return Response({'msg': 'send reply comment...'}, status=status.HTTP_201_CREATED)


class LikeReplyView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        user = User.objects.get(username=str(request.user))
        reply = ReplyComment.objects.get(id=pk)
        validation = LikeReply.objects.filter(user=user, reply=reply).exists()
        if validation:
                like = LikeReply.objects.get(user=user, reply=reply)
                like.delete()
        else:
            like = LikeReply.objects.get(user=user, reply=reply)
            like.like = True
            like.save()
        return Response({'msg': 'liked...'}, status=status.HTTP_201_CREATED)


class ShowReplyComment(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        post = Post.objects.get(id=pk)
        reply = ReplyComment.objects.filter(post=post)
        serializer = ReplyCommentSerializer(reply, many=True)
        like = LikeReply.objects.filter(reply=reply).count()
        content = {
            'reply': serializer.data,
            'like': like,
        }
        return Response(content, status=status.HTTP_200_OK)



class BookMarckView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        post = Posts.objects.get(id=pk)
        user = User.objects.get(username=str(request.user))
        validation = BookMarck.objects.filter(user=user).exists()
        if not validation:
            bookmarck = BookMarck.objects.create(user=user)
            bookmarck.post.add(post)
            bookmarck.save()
            return Response({'msg': 'add in bookmarck...'}, status=status.HTTP_201_CREATED)
        else:
            valid = BookMarck.objects.filter(user=user, post=post).exists()
            if valid:
                bookmarck = BookMarck.objects.create(user=user)
                bookmarck.post.remove(post)
                bookmarck.save()
                return Response({'msg': 'delete...'}, status=status.HTTP_200_OK)
            else:
                obj = BookMarck.objects.get(user=user)
                obj.post.add(post)
                obj.save()
                return Response({'msg': 'add in bookmarck...'}, status=status.HTTP_201_CREATED)


class AllBookMarckView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        query = BookMarck.objects.filter(user__username=str(request.user))
        serializer = BookMarckSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
