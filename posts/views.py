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
from posts.models import Posts, LikePost, Comment, LikeComment, ReplyComment, LikeReply
from accounts.renders import UserRender
from posts.serializers import (PostsSerializer, )


class ShowUserPost(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        post = Posts.objects.get(user__username=str(request.user))
        serializer = PostsSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShowOtherPosts(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        user = Profile.objects.get(id=pk)
        requester = User.objects.get(username=str(request.user))
        validation = Profile.objects.filter(id=pk, follower=requester).exists()
        # if requester.id in user.follower:
        if validation:
            post = Posts.objects.get(user__username=user)
            serializer = PostsSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'you cant see this page...'}, status=status.HTTP_400_BAD_REQUEST)

