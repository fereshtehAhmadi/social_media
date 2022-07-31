from rest_framework import serializers
from accounts.models import Profile, User, Validation
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


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


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class DeleteAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


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
            raise Serializer.VlidationError("password and confirm password doesn't match")
        return attrs


class RequestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Validation
        fields = ['phone', ]


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Validation
        fields = ['code', ]

