from rest_framework import serializers
from accounts.models import User, Validation, Request, Follower
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Validation
        fields = ['phone', ]

class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Validation
        fields = ['code', ]
    
    def validate(self, attrs):
        valid = self.context['valid'].code
        code = attrs.get('code')
        if code != valid :
            raise serializers.ValidationError("code was wrong!!")
        return attrs


class UserRegisterationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'}, write_only=True)
    code = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs={
            'password':{'write_only': True}
        }
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        
        if password != password2 :
            raise serializers.ValidationError("password and confirm password dosen't match!!")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        
        profile = Profile.objects.create(
            user = user
        )
        
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200)
    class Meta:
        model = User
        fields = ['username', 'password']


class UserResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, 
                                     style = {'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, 
                                     style = {'input_type': 'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']
    
    def validate(self, attrs):
        valid = self.context['user']
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if valid:
            if password != password2:
                raise Serializer.VlidationError("password and confirm password doesn't match!!")
            return attrs
        else:
            raise serializers.VlidationError("not found this phone number!!")


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, 
                                     style = {'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, 
                                     style = {'input_type': 'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise Serializer.VlidationError("password and confirm password doesn't match!!")
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'bio', 'cover', 'phone', ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['request', ]


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ['follower', ]
