from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path
from .views import RegisterView,UserDetailView

urlpatterns = [
    path("token/",TokenObtainPairView.as_view()),
    path("token/refresh/",TokenRefreshView.as_view()),
    path("signup/",RegisterView.as_view()),
    path("getme/",UserDetailView.as_view())
]