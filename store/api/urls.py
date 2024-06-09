from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path
from .views import RegisterView,UserDetailView,menu,topbarmenu,categoriesApi,searchApi,NavbarApi,courseUserApi,course_info,commentApi,getAllCourses,presell,alluser,getPopularCourses,ContactUsView,articleInfo,getAllArticles,categorySubCourses,banUserApi

urlpatterns = [
    path("token/",TokenObtainPairView.as_view(),name="login"),
    path("token/refresh/",TokenRefreshView.as_view(),name="refreshToken"),
    path("signup/",RegisterView.as_view()),
    path("getme/",UserDetailView.as_view()),
    path("menus/",menu.as_view()),
    path("menus/all/",NavbarApi.as_view(),name="panel_menus"),
    path("menus/topbar/",topbarmenu.as_view()),
    path("category/",categoriesApi.as_view()),
    path('search/<str:query>/', searchApi.as_view(), name='search'),
    path('courseuser/', courseUserApi.as_view(), name='courseUser'),
    path('courseinfo/<str:shortName>/', course_info.as_view(), name='course-info'),
    path('articleinfo/<str:href>/', articleInfo.as_view(), name='article-info'),
    path('category/<str:categoryName>/', categorySubCourses.as_view(), name='categorySubCourses'),
    path('comments/', commentApi.as_view(), name='comment'),
    path('allcourses/', getAllCourses.as_view(), name='allcourses'),
    path('allarticles/', getAllArticles.as_view(), name='allarticles'),
    path('courses/presell/', presell.as_view(), name='presell'),
    path('users/', alluser.as_view(), name='allUsers'),
    path('courses/popular/', getPopularCourses.as_view(), name='getPopular'),
    path('contact/', ContactUsView.as_view(), name='contactUs'),
    path('ban/<uuid:id>/', banUserApi.as_view(), name='banUser'),
]