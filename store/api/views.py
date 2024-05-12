from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer,UserSerializer,menuSerializer,coursesSerializer,categorySerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError,InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth import authenticate, get_user_model
from rest_framework.permissions import IsAuthenticated
from ..models import menus,courses,categories


user = get_user_model()
class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'access_token': str(refresh.access_token),
                # 'refresh_token' : str(refresh),
                "user":{
                'username': user.username,
                "email":user.email,
                "name":user.name,
                "role":user.role,
                "_id": user.id,
                "phone":user.phone
                }
            }
            return Response(response_data,status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class menu(APIView):
    def get(self,request):
        
        allMenus = menus.objects.all()
        serializer = menuSerializer(allMenus,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
#the 5 last created courses
class topbarmenu(APIView):
    def get(self,request):
        allcourses=courses.objects.all()
        print(allcourses)
        serializer = coursesSerializer(allcourses,many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)          

class categoriesApi(APIView):
    def get(self,request):
        allCategories = categories.objects.all()
        serializer=categorySerializer(allCategories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        


    



        


