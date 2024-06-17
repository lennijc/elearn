from django.contrib.auth.backends import ModelBackend  # Adjust the import path according to your project structure
from django.contrib.auth import authenticate, get_user_model
from .models import banUser  # Adjust the import path according to your project structure

class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        user = super().authenticate(request, username, password)
        if user and banUser.objects.filter(phone=user.phone).exists():
            return None  # Return None to indicate failure
        return user

    def get_user(self, user_id):
        user = super().get_user(user_id)
        if user and banUser.objects.filter(phone=user.phone).exists():
            return None  # Return None to indicate failure
        return user
    

User = get_user_model()

class EmailAuthBackend(object):
    """
    Authenticate using an e-mail address and check against banned phone numbers.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                # Check if the user's phone number is in the list of banned users
                if banUser.objects.filter(phone=user.phone).exists():
                    return None  # Return None to indicate failure
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            if banUser.objects.filter(phone=user.phone).exists():
                return None  # Return None to indicate failure
            return user
        except User.DoesNotExist:
            return None