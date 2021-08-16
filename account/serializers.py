from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser

User = get_user_model()


class RegisterApiSerializer(serializers.ModelSerializer, TokenObtainPairSerializer):
    password2 = serializers.CharField(min_length=6, required=True, write_only=True)
    access2 = serializers.CharField(min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ('access2', 'id', 'phone_number', 'password', 'password2', 'first_name', 'last_name', )

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs.get('password') != password2:
            raise serializers.ValidationError('Password and password2 did not match')
        if not attrs.get('password').isalnum():
            raise serializers.ValidationError('Password must contain alpha and numbers')
        phone_number = attrs.get('phone_number')
        user = authenticate(username=phone_number, password=password2)
        return attrs

    def to_representation(self, instance):
        representation = super(RegisterApiSerializer, self).to_representation(instance)
        refresh = self.get_token(instance)
        representation['refresh'] = str(refresh)
        representation['access'] = str(refresh.access_token)
        return representation

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(min_length=6, required=True, write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.pop('password', None)
        if not User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError('User not found')
        user = authenticate(username=phone_number, password=password)
        if user and user.is_active:
            refresh = self.get_token(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        else:
            raise serializers.ValidationError('Password or login is wrong')
        return attrs


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'city', 'country')
