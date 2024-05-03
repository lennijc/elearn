from typing import Any, Dict
from rest_framework import serializers
from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import password_validation, get_user_model

User = get_user_model()
class UserRegistrationSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email' , "password", "confirmPassword","name","phone","is_staff"]
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate(self, data):
        """
        Check that the password and confirm_password fields match.
        """
        password = data.get('password')
        confirmPassword = data.get('confirmPassword')

        if password and confirmPassword and password != confirmPassword:
            raise serializers.ValidationError({"confirmPassword": "Passwords must match."})

        return data

    def create(self, validated_data):
        try:
            is_staff = validated_data["is_staff"]
            role="A"
        except KeyError:
            role="U"
        # Remove the confirm_password field from the validated data

        validated_data.pop('confirmPassword', None)

        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    token_class = RefreshToken
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data=super().validate(attrs)
        data["user_id"]=self.user.id
        data["username"]=self.user.username
        data["phone"]=self.user.phone
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password'] #hashed password excluded