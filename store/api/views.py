from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from .serializers import UserRegistrationSerializer,UserSerializer,menuSerializer,coursesSerializer,categorySerializer,articleSerializer,NavbarCategoriesSerializer,courseuser,courseInfoSerializer,commentSerializer,AllCourseSerializer,ContactSerializer,articleInfoSerializer,AllArticleSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError,InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth import authenticate, get_user_model
from rest_framework.permissions import IsAuthenticated
from ..models import menus,courses,categories,article,courseUser
from authentication.models import banUser
from django.db import models
from django.db import IntegrityError


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
        serializer = coursesSerializer(allcourses,many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)          

class categoriesApi(APIView):
    def get(self,request):
        allCategories = categories.objects.all()
        serializer=categorySerializer(allCategories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class searchApi(APIView):
    def get(self,request,query):
        course_res=courses.objects.filter(
            name__icontains=query)|courses.objects.filter(
            description__icontains=query)
        article_res=article.objects.filter(
            title__icontains=query)|article.objects.filter(
            description__icontains=query)|article.objects.filter(
            href__icontains=query)
        course_serializer=coursesSerializer(course_res,many=True)
        article_serializer=articleSerializer(article_res,many=True)
        return Response({"courses":course_serializer.data,"articles":article_serializer.data})

class NavbarApi(APIView):
    def get(self,request):
        all_categories=categories.objects.all()
        serializer=NavbarCategoriesSerializer(all_categories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class courseUserApi(APIView):
    def get(self,request):
        all_courses=courseUser.objects.all()
        serializer=courseuser(all_courses,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class course_info(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,shortName):
        courseStudentsCount=courseUser.objects.filter(course__href=shortName).count()
        isUserRegisteredToThisCourse=True if courseUser.objects.filter(course__href=shortName,user=request.user) else False
        try:
            course=courses.objects.get(href=shortName)
        except:
            return Response({"DoesNotExist":f"course matching the query '{shortName}' does not exist"})
        serializer=courseInfoSerializer(course,context={"courseStudentsCount":courseStudentsCount,"isUserRegisteredToThisCourse":isUserRegisteredToThisCourse})
        return Response(serializer.data,status=status.HTTP_200_OK)

class commentApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        course_short_name = request.data.get('courseShortName')
        try:
            course = courses.objects.get(href=course_short_name)
            request.data["course"]=course.id
        except courses.DoesNotExist:
            return Response({"error": "Course short name not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = commentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course,creator=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class getAllCourses(APIView):
    def get(self,request):
        allCourses=courses.objects.all()
        serializer=AllCourseSerializer(allCourses,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class getAllArticles(APIView):
    def get(self,request):
        allarticles=article.objects.all()
        serializer=AllArticleSerializer(allarticles,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
       
class presell(APIView):
    def get(self,request):
        presell_courses = courses.objects.filter(isComplete=0)
        serializer=AllCourseSerializer(presell_courses,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
class alluser(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request):
        all_users = user.objects.all()
        all_user_serializer = UserSerializer(all_users,many=True)
        return Response(all_user_serializer.data , status=status.HTTP_200_OK)

class getPopularCourses(APIView):#base on the scores of each course
    def get(self,request):
        courses_with_scores =courses.objects.annotate(
        average_score=models.Avg(
            'comment__score', output_field=models.FloatField())).order_by('average_score')  # Ensure there are comment
        print(courses_with_scores)
        serializer=AllCourseSerializer(courses_with_scores,many=True)
        return Response(serializer.data)

class ContactUsView(APIView):
    def post(self, request, format=None):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class articleInfo(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,href):
        try:
            single_article=article.objects.get(href=href)
        except:
            return Response({"DoesNotExist":f"course matching the query '{href}' does not exist"})
        serializer=articleInfoSerializer(single_article)
        return Response(serializer.data,status=status.HTTP_200_OK)

class categorySubCourses(APIView):
    def get(self,request,categoryName):
        sub_courses = courses.objects.filter(categoryID__name=categoryName)
        sub_courses_serializer=AllCourseSerializer(sub_courses,many=True)
        return Response(sub_courses_serializer.data,status=status.HTTP_200_OK)
    

class banUserApi(APIView):
    permission_classes=[IsAdminUser]
    def put(self,requeset,id):
        ban_user=user.objects.get(id=id)
        try:
            banUser.objects.create(phone=ban_user.phone)
        except IntegrityError:
            return Response({"errorDetail":"maybe the user you are trying to ban has no phone number registered in the profile"})

        serializer=UserSerializer(ban_user)
        return Response({"bannedUserInfo":serializer.data})