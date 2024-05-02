from typing import Any, Dict
from rest_framework import serializers
from django.conf import settings
from core.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','username', 'email' , "password","is_staff"]
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        #inorder to determine the role of the user base on the is_staff provided by the client or not
        try:
            is_staff = validated_data["is_staff"]
            role="A"
        except KeyError:
            role="U"
        user = User.objects.create(
            name=validated_data['name'],
            username=validated_data['username'],
            email=validated_data['email'],
            is_staff=validated_data["is_staff"],
            role=role,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    token_class = RefreshToken
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data=super().validate(attrs)
        data["user_id"]=self.user.id
        data["username"]=self.user.username
        data["phone_nember"]=self.user.phone_number
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password'] #hashed password excluded