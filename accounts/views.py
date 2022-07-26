from rest_framework.views import APIView
from rest_framework import status, generics, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Count

from accounts.models import Profile
from accounts.renders import UserRender
from accounts.serializers import (UserRegisterationSerializer)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegisterationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Registration success...'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

