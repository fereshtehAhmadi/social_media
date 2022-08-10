from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status, generics, views, permissions
from rest_framework.response import Response

from django.contrib.auth import authenticate
from django.db.models import Count
from django.shortcuts import get_object_or_404

from accounts.models import User, Follower
from posts.models import (Posts, Gallery, LikePost, Comment, LikeComment,
                          ReplyComment, LikeReply, BookMarck)
from accounts.renders import UserRender
from posts.serializers import (PostsSerializer, GallerySerializer, CreatePostSerializer,
                               CreateCommentSerializer, ReplyCommentSerializer, BookMarckSerializer,
                               CommentSerializer, CreateReplyCommentSerializer, UpdatePostSerializer,
                               LikePostSerializer, LikeCommentSerializer, LikeReplySerializer)


class ShowUserPost(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        post = Posts.objects.filter(user=request.user.id)
        
        for p in post:
            g = Gallery.objects.filter(post=p).first()
            g.selected = True
            g.save()
        
        gallery = Gallery.objects.filter(post__user__id=request.user.id, selected=True)  
        serializer_gallery = GallerySerializer(gallery, many=True)
        
        content = {
            'gallery': serializer_gallery.data,
        }
        return Response(content, status=status.HTTP_200_OK)


class ShowOtherPosts(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        user = User.objects.get(id=pk)
        requester = User.objects.get(id=request.user.id)
        validation = Follower.objects.filter(user=user, follower=requester).exists()
        if validation:
            post = Posts.objects.filter(user=user)
            for p in post:
                g = Gallery.objects.filter(post=p).first()
                g.selected = True
                g.save()
            
            gallery = Gallery.objects.filter(post__user=user, selected=True)
            serializer_gallery = GallerySerializer(gallery, many=True)
            
            content = {
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
        requester = User.objects.get(id=request.user.id)
        validation = Follower.objects.filter(user=post.user, follower=requester).exists()
        if validation or post.user == requester:
            post = Posts.objects.get(id=pk)
            post.views = int(post.views) + 1
            post.save()
            serializer_post = PostsSerializer(post)
            gallery = Gallery.objects.filter(post=post)
            serializer_gallery = GallerySerializer(gallery, many=True)
            
            like = LikePost.objects.filter(post=post).count()
            comment = Comment.objects.filter(post=post).count()
            reply = ReplyComment.objects.filter(comment__post=post).count()
            comment_num = int(comment) + int(reply)
            content = {
            'post': serializer_post.data,
            'gallery': serializer_gallery.data,
            'like': like,
            'comment': comment_num,
            }
            
            return Response(content, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'you cant see this post...'}, status=status.HTTP_400_BAD_REQUEST)        


class CreatePost(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, fromat=None):
        serializer = CreatePostSerializer(data=request.data, context={'request':request,})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePost(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        post = Posts.objects.get(id=pk)
        requester = User.objects.get(id=request.user.id)
        validation = Follower.objects.filter(user=post.user, follower=requester).exists()
        if post.user == requester:
            post = Posts.objects.get(id=pk)
            serializer = PostsSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request, pk, format=None):
        user = User.objects.get(id=request.user.id)
        post = Posts.objects.get(id=pk)
        if post.user == user:
            serializer = UpdatePostSerializer(data=request.data)
            post.content = request.data.get('content')
            post.save()
            return Response({'msg': 'update successfully...'}, status=status.HTTP_201_CREATED)
        return Response({'msg': 'something wrong!!'}, status=status.HTTP_404_NOT_FOUND)


class DeletePost(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk, format=None):
        user = User.objects.get(id=request.user.id)
        post = Posts.objects.get(id=pk)
        if post.user == user:
            post.delete()
            post.save()
            return Response({'msg': 'delete successfully...'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'msg': 'not found...'}, status=status.HTTP_404_NOT_FOUND)


class LikePostView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        user = User.objects.get(id=request.user.id)
        post = Posts.objects.get(id=pk)
        validation = LikePost.objects.filter(user=user, post=post).exists()
        if validation:
                like = LikePost.objects.get(user=user, post=post)
                like.delete()
                msg = 'dislike...'
        else:
            like = LikePost.objects.create(user=user, post=post, like=True)
            msg = 'liked...'
            
        return Response({'msg': msg}, status=status.HTTP_201_CREATED)


class ShowLikePostList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        post = Posts.objects.get(id=pk)
        like = LikePost.objects.filter(post=post)
        serializer = LikePostSerializer(like, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateCommentView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        user = User.objects.get(id=request.user.id)
        post = Posts.objects.get(id=pk)
        serializer = CreateCommentSerializer(data=request.data)
        Comment.objects.create(user=user, post=post, content=request.data.get('content'))
        return Response({'msg': 'send comment...'}, status=status.HTTP_201_CREATED)


class LikeCommentView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        validation = LikeComment.objects.filter(user__id=request.user.id, comment__id=pk).exists()
        if validation:
                like = LikeComment.objects.get(user__id=request.user.id, comment__id=pk)
                like.delete()
                msg = 'deslike...'
        else:
            like = LikeComment.objects.create(user__id=request.user.id, comment__id=pk, like=True)
            msg = 'liked...'
        return Response({'msg': msg}, status=status.HTTP_201_CREATED)


# class ShowComment(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, pk, format=None):
#         post_obj = get_object_or_404(Posts, pk=pk)
#         post_comments = post_obj.comment_set.all()
#         # comment = Comment.objects.filter(post__id=pk)
#         serializer = CommentSerializer(post_comments, many=True)
#         comment_obj = {'comment': comment for comment in post_comments}
#         like = LikeComment.objects.filter(**comment_obj).count()
#         content = {
#             'comment': serializer.data,
#             'like': like,
#         }
#         return Response(content, status=status.HTTP_200_OK)


class ShowComment(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        comment_list = Comment.objects.filter(post__id=pk)
        comments = {}
        for comment in comment_list:
            like_comment = LikeComment.objects.filter(comment=comment).count()
            user_dict = vars(comment.user)
            replys = {}
            reply_list = ReplyComment.objects.filter(comment=comment)
            
            for reply in reply_list:
                like_reply = LikeReply.objects.filter(reply=reply).count()
                reply_id = reply.id
                user2_dict = vars(reply.user)
                rep = {reply.id:reply.content, f'time{reply_id}':comment.create, f'user_id{reply_id}':user2_dict["id"], f'user_username{reply_id}':user2_dict["username"], f'like{reply_id}':like_reply}
                replys.update(rep)
                print(replys)
                
            comment_id= comment.id   
            comment_obj = {comment_id:comment.content, f'time{comment_id}':comment.create, f'user_id{comment_id}':user_dict["id"], f'user_username{comment_id}':user_dict["username"], f'like{comment_id}':like_comment, f'replys{comment_id}':replys}
            reply_list = ReplyComment.objects.filter(comment=comment)
            comments.update(comment_obj)
                
        content = {
            'comment': comments,
        }
        return Response(content, status=status.HTTP_200_OK)


class DeleteComment(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk, format=None):
        comment = Comment.objects.get(id=pk)
        user = User.objects.get(id=request.user.id)
        post = Posts.objects.get(id=comment.post.id)
        if comment.user == user or post.user == user:
            comment.delete()
            return Response({'msg': 'delete comment successfully...'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'msg': ':/ ?!'}, status=status.HTTP_404_NOT_FOUND)


class ShowLikeCommentList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        comment = Comment.objects.get(id=pk)
        like = LikeComment.objects.filter(comment=comment)
        serializer = LikeCommentSerializer(like, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReplyCommentView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        user = User.objects.get(id=request.user.id)
        comment = Comment.objects.get(id=pk)
        serializer = CreateReplyCommentSerializer(data=request.data)
        ReplyComment.objects.create(user=user, comment=comment, content=request.data.get('content'))
        return Response({'msg': 'send reply comment...'}, status=status.HTTP_201_CREATED)


class LikeReplyView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        user = User.objects.get(id=request.user.id)
        reply = ReplyComment.objects.get(id=pk)
        validation = LikeReply.objects.filter(user=user, reply=reply).exists()
        if validation:
                like = LikeReply.objects.get(user=user, reply=reply)
                like.delete()
                msg="dislike..."
        else:
            like = LikeReply.objects.create(user=user, reply=reply, like=True)
            msg='like...'
        
        return Response({'msg': msg}, status=status.HTTP_201_CREATED)


class DeleteReplyComment(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk, format=None):
        user = User.objects.get(id=request.user.id)
        comment = ReplyComment.objects.get(id=pk)
        post = Posts.objects.get(id=comment.post)
        if comment.user == user or post.user == user:
            comment.delete()
            comment.save()
            return Response({'msg': 'delete comment successfully...'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'msg': ':/ ?!'}, status=status.HTTP_404_NOT_FOUND)


class ShowLikeReplyList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        comment = ReplyComment.objects.get(id=pk)
        like = LikeReply.objects.get(reply=comment)
        serializer = LikeReplySerializer(like, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class ShowReplyComment(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, pk, format=None):
#         reply = ReplyComment.objects.filter(comment__id=pk)
#         serializer = ReplyCommentSerializer(reply, many=True)
#         reply_obj = {'reply': rep for rep in reply}
#         like = LikeReply.objects.filter(**reply_obj).count()
        
#         content = {
#             'reply': serializer.data,
#             'like': like,
#         }
#         return Response(content, status=status.HTTP_200_OK)


class BookMarckView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        post = Posts.objects.get(id=pk)
        user = User.objects.get(id=request.user.id)
        valid = Follower.objects.filter(user=post.user, follower=user).exists()
        if valid:
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
                    return Response({'msg': 'remove this post from bookmarck...'}, status=status.HTTP_200_OK)
                else:
                    obj = BookMarck.objects.get(user=user)
                    obj.post.add(post)
                    obj.save()
                    return Response({'msg': 'add in bookmarck...'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': 'you can`t bookmarck this post!!!'})

class AllBookMarckView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        query = BookMarck.objects.filter(user__id=request.user.id)
        serializer = BookMarckSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
