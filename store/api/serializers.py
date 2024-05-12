from typing import Any, Dict
from rest_framework import serializers
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import password_validation, get_user_model
from ..models import menus,courses,categories
User = get_user_model()

class menuSerializer(serializers.ModelSerializer):
    class Meta:
        model=menus
        fields="__all__"

class coursesSerializer(serializers.ModelSerializer):
    class Meta:
        model=courses
        fields="__all__"

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model=categories
        fields="__all__"
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
            
            if validated_data["is_staff"]:
                validated_data["role"]="ADMIN"
            else:
                validated_data["role"]="USER"
            
        except KeyError:
            #if no is_staff provided by the user then it has to put the default value for the role which is user
            validated_data["role"]="USER"
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
    def to_internal_value(self, data):
        return super().to_internal_value(data)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password'] #hashed password excluded
        
