from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status, generics, views, permissions
from rest_framework.response import Response

from random import randint

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.db.models import Count

from accounts.models import Profile, User, Validation
from accounts.renders import UserRender
from accounts.serializers import (UserRegisterationSerializer, UserLoginSerializer,
    DeleteAccountSerializer,UserSerializer,ProfileSerializer, UserInfoSerializer, 
    ProfileInfoSerializer, UserChangePasswordSerializer, PhoneSerializer, CodeSerializer)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def kave_negar_token_send(receptor, code):
    try:
        api = KavenegarAPI(API_KEY)
        params = {
            'receptor': receptor,
            'template': 'your_template',
            'token': token
        }
        response = api.verify_lookup(params)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


# class UserRegisterationView(APIView):
#     permission_classes = (permissions.AllowAny,)
#     def post(self, request, format=None):
#         token = randint(1000, 9999)
#         kave_negar_token_send(request.data.get('phone'), token)
#         serializer = UserRegisterationSerializer(data=request.data, context={'request': token})
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.save()
#             return Response({'msg':'Registration success...'}, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

class SendPhoneNumber(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token = randint(1000, 9999)
            valid = serializer.save()
            valid.code = token
            valid.save()
            kave_negar_token_send(request.data.get('phone'), token)
            return Response(valid.id, status=status.HTTP_201_CREATED)


class Validate(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, pk, format=None):
        valid = Validation.objects.get(id=pk)
        serializer = CodeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            print(valid.code)
            if serializer.data.get('code') == valid.code:
                return Response({'status':True, 'id': valid.id}, status=status.HTTP_200_OK)
        return Response({'status':False}, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterationView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, status, pk, format=None):
        if status == 'True':
            serializer = UserRegisterationSerializer(data=request.data, context={'request': token})
            if serializer.is_valid(raise_exception=True):
                valid = Validation.objects.get(id=pk)
                user = serializer.save()
                user.phone = valid.phone
                user.save()
                return Response({'msg':'Registration success...'}, status=status.HTTP_201_CREATED)
            
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


class UserChangePasswordView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(username=str(request.user))
            user.set_password(request.data.get('password'))
            user.save()
            return Response({'msg': 'your password is change...'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEditView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, format=None):
        user = UserSerializer(data=request.data)
        if user.is_valid(raise_exception=True):
            user.save()
            profile = ProfileSerializer(data=request.data)
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
        follower = profile.follower.all().count()
        following = profile.following.all().count()
        content = {
            'user': user_info.data,
            'profile' : profile_info.data,
            'follower': follower,
            'following': following,
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


class SendRequest(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        sender = User.objects.get(username=str(request.user))
        receiver = User.objects.get(id=pk)
        receiver_profile = Profile.objects.get(user__username=receiver)
        receiver_profile.request.add(sender)
        receiver_profile.save()
        return Response({'msg': 'your request has been sent...'}, status=status.HTTP_200_OK)


class AcceptRequest(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, status, format=None):
        sender = User.objects.get(id=pk)
        sender_profile = Profile.objects.get(user=sender)
        user = User.objects.get(username=str(request.user))
        user_profile = Profile.objects.get(user=user)
        if status == 'True':
            user_profile.follower.add(sender)
            user_profile.request.remove(sender)
            user_profile.save()
            sender_profile.following.add(user)
            sender_profile.save()
            return Response({'msg': 'you accept the request...'})
        elif status == 'False':
            user_profile.request.remove(sender)
            user_profile.save()
            return Response({'msg': 'you delete the request...'})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RequestList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = Profile.objects.get(user__username=str(request.user))
        serializer = ProfileSerializer(user)
        
        content = {
            'requests': serializer.data.get('request')
        }
        return Response(content, status=status.HTTP_200_OK)


class Unfollow(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, pk, format=None):
        me = User.objects.get(username=str(requset.user))
        me_profile = Profile.objects.get(user__username=me.username)
        user = User.objects.get(id=pk)
        profile = Profile.objects.get(user__username=user.username)
        profile.following.remove(me)
        me_profile.follower.remove(profile)
        return Response({'msg': 'Unfollow...'}, status=status.HTTP_200_OK)


class Block(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, pk, format=None):
        me = User.objects.get(username=str(request.user))
        me_profile = Profile.objects.get(user=me)
        user = User.objects.get(id=pk)
        profile = Profile.objects.get(user__username=user.username)
        profile.follower.remove(me)
        me_profile.following.remove(user)
        return Response({'msg': 'Blocked...'}, status=status.HTTP_200_OK)


class FollowerList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None, format=None):
        if pk is None:
            user = Profile.objects.get(user__username=str(request.user))
            serializer = ProfileSerializer(user)
        else:
            user = Profile.objects.get(id=pk)
            serializer = ProfileSerializer(user)
        
        content = {
            'follower': serializer.data.get('follower')
        }
        return Response(content, status=status.HTTP_200_OK)


class FollowingList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None, format=None):
        if pk is None:
            user = Profile.objects.get(user__username=str(request.user))
            serializer = ProfileSerializer(user)
        else:
            user = Profile.objects.get(id=pk)
            serializer = ProfileSerializer(user)
        
        content = {
            'following': serializer.data.get('following')
        }
        return Response(content, status=status.HTTP_200_OK)


class UserInfo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        user = User.objects.get(id=pk)
        user_serializer = UserSerializer(user)
        profile = Profile.objects.get(user__username=user)
        profile_serializer = ProfileSerializer(profile)
        follower = profile.follower.all().count()
        following = profile.following.all().count()
        
        content = {
            'user': user_serializer.data,
            'profile': profile_serializer.data,
            'follower': follower,
            'following': following,
        }
        return Response(content, status=status.HTTP_200_OK)
