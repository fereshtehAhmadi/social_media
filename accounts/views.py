from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status, generics, views, permissions
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.db.models import Count

from accounts.models import Profile
from accounts.renders import UserRender
from accounts.serializers import (UserRegisterationSerializer, UserLoginSerializer,
    DeleteAccountSerializer,UserEditSerializer,ProfileEditSerializer, UserInfoSerializer, 
    ProfileInfoSerializer)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegisterationView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Registration success...'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                login(request, user)
                return Response({'token':token, 'msg':'login success...'}, status=status.HTTP_200_OK)
        
        return Response({'errors': {'non_field_errors':['username or password is not valid!!']}},
                        status=status.HTTP_404_NOT_FOUND)


class UserEditView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, format=None):
        user = UserEditSerializer(data=request.data)
        if user.is_valid(raise_exception=True):
            user.save()
            profile = ProfileEditSerializer(data=request.data)
            if profile.is_valid(raise_exception=True):
                profile.save()
                content = {
                    'user': user.data,
                    'profile': profile.data,
                }
                return Response(content, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(profile.errors, status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user.errors, status= status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, format=None):
        query = User.objects.get(username=str(request.user))
        user_info = UserInfoSerializer(query)
        profile = Profile.objects.get(user=query)
        profile_info = ProfileInfoSerializer(profile)
        content = {
            'user': user_info.data,
            'profile' : profile_info.data,
        }
        return Response(content, status.HTTP_200_OK)


class UserLogoutView(generics.GenericAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDeleteAccountView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request):
            serializer = DeleteAccountSerializer(data=request.data)
            id = serializer.data.get('id')
            user = User.objects.get(id=id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

