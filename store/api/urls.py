from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path
from .views import RegisterView,UserDetailView,menu,topbarmenu,categoriesApi,searchApi,NavbarApi,courseUserApi,course_info

urlpatterns = [
    path("token/",TokenObtainPairView.as_view()),
    path("token/refresh/",TokenRefreshView.as_view()),
    path("signup/",RegisterView.as_view()),
    path("getme/",UserDetailView.as_view()),
    path("menus/",menu.as_view()),
    path("menus/all/",NavbarApi.as_view(),name="panel_menus"),
    path("menus/topbar/",topbarmenu.as_view()),
    path("category/",categoriesApi.as_view()),
    path('search/<str:query>/', searchApi.as_view(), name='search'),
    path('courseuser/', courseUserApi.as_view(), name='courseUser'),
    path('courseinfo/<str:shortName>/', course_info.as_view(), name='course-info'),

]