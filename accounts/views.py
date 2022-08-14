from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status, generics, views, permissions, mixins
from rest_framework.response import Response

from random import randint
from kavenegar import *
from social_media.settings import kave_negar_token_send

from api_list import api_list

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.db.models import Count

from accounts.models import User, Validation, Request, Follower
from accounts.renders import UserRender
from accounts.serializers import (UserRegisterationSerializer, CodeSerializer, PhoneSerializer,
    UserLoginSerializer, UserResetPasswordSerializer, UserChangePasswordSerializer,
    UserProfileSerializer, UserSerializer, SearchUserSerializer, RequestSerializer,
    FollowerSerializer)



class ApiListView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):         
        return Response(api_list)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class SendPhoneNumber(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            code = randint(1000, 9999)
            valid = serializer.save()
            valid.code = code
            valid.save()
            kave_negar_token_send(serializer.data['phone'], int(code))
            return Response(valid.id, status=status.HTTP_201_CREATED)


class RegisterationView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, pk, format=None):
        valid = Validation.objects.get(id=pk)
        serializer = CodeSerializer(data=request.data, context={'valid': valid})
        if serializer.is_valid(raise_exception=True):
            serializer2 = UserRegisterationSerializer(request.data)
            if serializer2.is_valid(raise_exception=True):
                serializer2.save()
                valid.delete()
                return Response(serializer2.data, status=status.HTTP_200_OK)
        return Response({'msg': 'your code is wrong!!'}, status=status.HTTP_400_BAD_REQUEST)


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


class UserResetPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, pk, format=None):
        valid = Validation.objects.get(id=pk)
        serializer = CodeSerializer(data=request.data, context={'valid': valid})
        if serializer.is_valid(raise_exception=True):
            user = User.objects.filter(phone=valid.phone).exists()
            serializer2 = UserResetPasswordSerializer(data=request.data, context={'user': user})
            if serializer2.is_valid(raise_exception=True):
                reset = User.objects.get(phone=valid.phone)
                reset.set_password(request.data.get('password'))
                reset.save()
                valid.delete()
                return Response({'msg': 'your password is reset...'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserChangePasswordView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            reset = User.objects.get(username=request.user)
            reset.set_password(request.data.get('password'))
            reset.save()
            return Response({'msg': 'your password is change...'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(user.errors, status= status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        user_info = UserProfileSerializer(user)
        follower_count = Follower.objects.filter(user=user).count()
        following_count = Follower.objects.filter(follower=user).count()
        content = {
            'user': user_info.data,
            'follower': follower_count,
            'following': following_count,
            'button': 'Edit Information',
        }
        return Response(content, status.HTTP_200_OK)


# -----------------------------------------------------------------------
# class ProfileViewSet(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def patch(self, request): # change this to use the patch mixin
#         profile = Profile.objects.filter(user = request.user).first()
#         profile.first_name = request.data['first_name']
#         profile.last_name = request.data['last_name']
#         profile.bio = request.data['bio']
#         profile.location = request.data['location']
#         profile.save()
#         return JsonResponse({"response": "change successful"})
# --------------------------------------------------------------------------


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
            serializer = UserSerializer(data=request.data)
            id = serializer.data.get('id')
            user = User.objects.get(id=id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class SearchUser(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, search, format=None):
        user = User.objects.filter(username__icontains=search)
        serializer = SearchUserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendRequest(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        requester = User.objects.get(username=str(request.user))
        valid = Request.objects.filter(user__id=pk).exists()
        if valid:
            receiver.request = requester
            receiver.save()
        else:
            Request.objects.create(user__id=pk, request=requester)
        return Response({'msg': 'your request has been sent...'}, status=status.HTTP_200_OK)


class RequestListView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        request_num = Request.objects.filter(user=user).count()        
        request_list = Request.objects.filter(user=user)
        # serializer = RequestSerializer(request_list, many=True)
        requests = {}
        for request in request_list:
            user_dict = vars(request.request)
            user = {user_dict["id"]: user_dict["username"]}
            requests.update(user)
        content = {
            'request_list': requests,
            'request_num': request_num,
        }
        return Response(content, status=status.HTTP_200_OK)


class AcceptRequest(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, status, format=None):
        sender = User.objects.get(id=pk)
        request = Request.objects.get(request=sender)
        user = User.objects.get(id=request.user.id)
        if status == 1:
            Follower.objects.create(user=user, follower=sender)
            request.delete()
            return Response({'msg': 'you accept the request...'})
        
        elif status == 0:
            request.delete()
            return Response({'msg': 'you delete the request...'})
        return Response({'msg': ':)'})


class UnFollowUserView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, pk, format=None):
        user = User.objects.get(id=pk)
        follower = User.objects.get(id=request.user.id)
        request = Follower.objects.filter(user=user, follower=follower).first()
        request.delete()
        return Response({'msg': f'you unfollow {user.username} ...'}, status=status.HTTP_200_OK)


class DeleteFollowerView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, pk, format=None):
        user = User.objects.get(id=request.user.id)
        follower = User.objects.get(id=pk)
        request = Follower.objects.filter(user=user, follower=follower).first()
        request.delete()
        content = {
            'delete': f'you delete from your following list {user.username} ...',
        }
        return Response(content, status=status.HTTP_200_OK)


class BlockView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, pk, format=None):
        me = User.objects.get(id=request.user.id)
        follower = User.objects.get(id=pk)
        block1 = Follower.objects.filter(user=me, follower=follower).first()
        block2 = Follower.objects.filter(user=follower, follower=me).first()
        if block1:
            block1.delete()
        if block2:
            block2.delete()
        return Response({'msg': 'Blocked...'}, status=status.HTTP_200_OK)


class MyFollowerList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        follower_list = Follower.objects.filter(user=user)
        # serializer = FollowerSerializer(follower_list, many=True)
        num = Follower.objects.filter(user=user).count()
        followers = {}
        for follower in follower_list:
            user_dict = vars(follower.follower)
            user = {user_dict["id"]: user_dict["username"]}
            followers.update(user)
        
        content = {
            'follower': followers,
            'number': num,
        }
        return Response(content, status=status.HTTP_200_OK)


class FollowerList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None, format=None):
        user = User.objects.get(id=pk)
        follower_list = Follower.objects.filter(user=user)
        # serializer = FollowerSerializer(follower_list, many=True)
        num = Follower.objects.filter(user=user).count()
        followers = {}
        for follower in follower_list:
            user_dict = vars(follower.follower)
            user = {user_dict["id"]: user_dict["username"]}
            followers.update(user)
        
        content = {
            'follower': followers,
            'number': num,
        }
        return Response(content, status=status.HTTP_200_OK)


class MyFollowingList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        following_list = Follower.objects.filter(follower=user)
        # serializer = FollowerSerializer(following_list, many=True)
        num = Follower.objects.filter(follower=user).count()
        
        followings = {}
        for following in following_list:
            user_dict = vars(following.user)
            user = {user_dict["id"]: user_dict["username"]}
            followings.update(user)
            
        content = {
            'following': followings,
            'number': num,
        }
        return Response(content, status=status.HTTP_200_OK)


class FollowingList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None, format=None):
        user = User.objects.get(id=pk)
        following_list = Follower.objects.filter(follower=user)
        # serializer = FollowerSerializer(following_list, many=True)
        num = Follower.objects.filter(follower=user).count()
        followings = {}
        for following in following_list:
            user_dict = vars(following.user)
            user = {user_dict["id"]: user_dict["username"]}
            followings.update(user)
        
        content = {
            'following': followings,
            'number': num,
        }
        return Response(content, status=status.HTTP_200_OK)


class UserProfile(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        me = User.objects.get(id=request.user.id)
        user = User.objects.get(id=pk)
        serializer = UserProfileSerializer(user)
        follower_count = Follower.objects.filter(user=user).count()
        following_count = Follower.objects.filter(follower=user).count()
        
        if Follower.objects.filter(user=user, follower=me).exists():
            button = 'UnFollow'
        elif pk == request.user.id:
            button = 'Edit Information'
        else:
            button = 'Follow'
         
        content = {
            'profile': serializer.data,
            'follower': follower_count,
            'following': following_count,
            'button': button,
        }
        return Response(content, status=status.HTTP_200_OK)
