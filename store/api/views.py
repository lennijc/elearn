from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from.serializers import (UserRegistrationSerializer,UserSerializer,menuSerializer,coursesSerializer,categorySerializer,
    articleSerializer,NavbarCategoriesSerializer,courseuserSerializer,courseInfoSerializer,commentSerializer,AllCourseSerializer,
    ContactSerializer,articleInfoSerializer,AllArticleSerializer,categorySubMenu,EmailSerializer,
    ChangePasswordSerializer,userProfileSerializer,
    answerCommentSerializer,offSerializer,sessionSerializer,simpleSessionSerialzier,contactSerializer)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError,InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.generics import RetrieveAPIView,CreateAPIView
from django.contrib.auth import authenticate, get_user_model
from rest_framework.permissions import (IsAuthenticated,IsAuthenticatedOrReadOnly,
                                        IsAdminUser,BasePermission,SAFE_METHODS)
from ..models import menus,courses,categories,article,courseUser,comment,session,off,contact
from authentication.models import banUser
from django.db import models
from django.db import IntegrityError
from rest_framework.generics import DestroyAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework import viewsets
from store.tasks import send_notification_mail
from django.db.models import Sum
from datetime import timedelta
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
import os

user = get_user_model()

#a custom permission to be able to use the viewset apis both for cms and mainpage
class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow safe methods for everyone
        if request.method in SAFE_METHODS:
            return True
        
        # Admin users can perform any operation
        return request.user and request.user.is_staff
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
        course_serializer=AllCourseSerializer(course_res,many=True)
        article_serializer=AllArticleSerializer(article_res,many=True)
        return Response({"courses":course_serializer.data,"articles":article_serializer.data})

class NavbarApi(APIView):
    def get(self,request):
        all_categories=categories.objects.all()
        serializer=NavbarCategoriesSerializer(all_categories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class courseUserApi(APIView):
    def get(self,request):
        all_courses=courseUser.objects.all()
        serializer=courseuserSerializer(all_courses,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class course_info(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]
    def get(self,request,shortName):
        courseStudentsCount=courseUser.objects.filter(course__href=shortName).count()
        if self.request.user.is_authenticated:
            isUserRegisteredToThisCourse=True if courseUser.objects.filter(course__href=shortName,user=request.user) else False
        else:
            isUserRegisteredToThisCourse=False
        try:
            course=courses.objects.get(href=shortName)
        except:
            return Response({"DoesNotExist":f"course matching the query '{shortName}' does not exist"})
        serializer=courseInfoSerializer(course,context={"courseStudentsCount":courseStudentsCount,"isUserRegisteredToThisCourse":isUserRegisteredToThisCourse})
        return Response(serializer.data,status=status.HTTP_200_OK)

class SendCommentApi(APIView):
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
        allCourses=courses.objects.all().order_by("-createdAt")
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
    permission_classes=[IsAuthenticatedOrReadOnly]
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
    
class navbarWithSubMenu(APIView):
    def get(self,request):
        allCategories=categories.objects.all()
        serializer=categorySubMenu(allCategories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class deleteUserApi(DestroyAPIView):
    queryset = user.objects.all()
    permission_classes=[IsAdminUser]
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs) 

class getAllComments(APIView):
    def get(self,request):
        all_comments = comment.objects.all()
        comment_serializer = commentSerializer(all_comments,many=True)
        return Response(comment_serializer.data,status=status.HTTP_200_OK)

class categoryViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=categories.objects.all()
    serializer_class=categorySerializer


class sendContactAnswer(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,*args,**kwargs):
        serailizer=EmailSerializer(data=request.data)
        serailizer.is_valid(raise_exception=True)
        email=serailizer.validated_data["email"]
        message=serailizer.validated_data["message"]
        send_notification_mail(email,message)
        return Response({"email task queued"},status=status.HTTP_201_CREATED)
    
class orderlistApiView(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=courseuserSerializer
    def get_queryset(self):   
        queryset = courseUser.objects.filter(user=self.request.user)
        return queryset
    
class orderRetrieveApiView(RetrieveAPIView):
    queryset=courseUser.objects.all()
    serializer_class=courseuserSerializer


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        
        if not object.check_password(serializer.validated_data["old_password"]):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        object.set_password(serializer.validated_data["new_password"])
        object.save()
        return Response({"message":"password changed successfully"},status=status.HTTP_200_OK)

class UserAPIView(UpdateAPIView):
    serializer_class = userProfileSerializer
    permission_classes = (IsAuthenticated,)
    def get_object(self):
        return self.request.user
    
class getMainPageInfo(APIView):
    def get(self,request):
        _courses_count = courses.objects.all().count()
        _total_sessions_time=session.objects.aggregate(total_time=Sum("time"))
        total_duration_readable=0
        print(_total_sessions_time)
        if _total_sessions_time:
            try:
                total_duration_readable = str(timedelta(seconds=int(_total_sessions_time["total_time"].total_seconds())))
                print(f"Total Duration (HH:MM:SS): {total_duration_readable}")
            except AttributeError:
                print("there is no session video in the site")
        else:
            print("No sessions found.")
            _total_sessions_time["total_time"]=0
        _email="storino@gmail.com"
        _phone="02199339339"
        _users_count=user.objects.all().count()
        _response_data={
            "coursesCount":_courses_count,
            "email":_email,
            "phone":_phone,
            "totalTime":(0 if _total_sessions_time["total_time"]==0 or _total_sessions_time["total_time"]==None
                        else int(_total_sessions_time["total_time"].total_seconds()/60)),
            "usersCount":_users_count,
        }
        return Response(_response_data,status=status.HTTP_200_OK)
    

class coursesViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAdminUser]
    queryset=courses.objects.all()
    serializer_class=coursesSerializer
    parser_classes=[MultiPartParser]
    def perform_create(self, serializer):
        return serializer.save(creator=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except Exception as e:
            return Response({"course deletion didn't happen likely they are students already enrolled in this course":str(e)},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"successfully done"},status=status.HTTP_202_ACCEPTED)

class articleViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAdminUser]
    queryset=article.objects.all()
    serializer_class=articleSerializer


class createPublishArticle(CreateAPIView):
    permission_classes=[IsAdminUser]
    serializer_class=articleSerializer
    parser_classes=[MultiPartParser]
    def perform_create(self, serializer):
        serializer.validated_data["publish"]=True
        serializer.validated_data["creator"]=self.request.user
        serializer.save()
    
    def get_queryset(self):
        return article.objects.all().select_related("category")
        

class createDraftArticle(CreateAPIView):
    permission_classes=[IsAdminUser]
    serializer_class=articleSerializer
    parser_classes=[MultiPartParser]
    queryset=article.objects.all()
    def perform_create(self, serializer):
        serializer.validated_data["creator"]=self.request.user
        serializer.save()
    
class changeUserRole(APIView):
    def put(self, request, format=None):
        user_id = request.data.get('id')  # Extract user ID from request data
        try:
            instance = user.objects.get(id=user_id)  # Fetch user instance
        except user.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        print("request.data is : " , request.data)
        serializer = UserSerializer(instance=instance,data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        print(serializer.data)
        return Response(serializer.data,status=status.HTTP_200_OK)

class publishDraftArticle(UpdateAPIView):
    queryset = article.objects.all()
    serializer_class = articleSerializer
    permission_classes=[IsAdminUser]
    parser_classes=[MultiPartParser]
    def get_object(self):
        print("self.kwargs is : " , self.kwargs , "and args is: ",self.args)
        print("self.request is : " , self.request)
        href = self.kwargs['href']
        try:
            return article.objects.get(href=href)
        except article.DoesNotExist:
            return None

    def perform_update(self, serializer):
        serializer.save(publish=True)
        
    
class commentViewSet(viewsets.ModelViewSet):
    serializer_class=answerCommentSerializer
    permission_classes=[IsAdminUser]
    queryset=comment.objects.all()
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions this view requires.
        """
        if self.action == 'answerComment':
            self.permission_classes = [IsAuthenticated]  # Allow all users to answer comments
        else:
            self.permission_classes = [IsAdminUser]  # Restrict other actions to admin users
        return super().get_permissions()
    
    @action(detail=True, methods=["post"])
    def answerComment(self, request, *args, **kwargs):
        mainCommentID = self.kwargs["pk"]
        mainCommentInstance = get_object_or_404(comment, pk=mainCommentID)
        mainCommentInstance.answer=1
        mainCommentInstance.save()
        # also we could add the new comment data to the request.data and pass the data to the self.create(request)
        #the answer has to inherit the course or article from the mainCommentInstance as this is an answer to that mainComment
        answer_comment_data = {
            "mainCommentID": mainCommentID,
            "creator": request.user.id, 
            "body":request.data["body"],
            "course": mainCommentInstance.course_id,  
            "article": mainCommentInstance.article_id,
            "answer": 1,
            "isAnswer": True,
            "score": 5,
        }
        serializer = self.get_serializer(data=answer_comment_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    #accepting comment mean that we set the answer field of comment instance to one and will be visible in the client side
    @action(methods=['put'], detail=True)
    def accept_reject_comment(self, request,*args,**kwargs):
        """
        Toggle the 'answer' field of a comment.
        """
        try:
            comment = self.get_object()
            comment.answer = not comment.answer  # Toggle the answer field
            comment.save()
            serializer=commentSerializer(comment)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class offViewset(viewsets.ModelViewSet):
    permission_classes=[IsAdminUser]
    serializer_class=offSerializer
    queryset=off.objects.all()
    def create(self, request, *args, **kwargs):
        #we dont send the client the creator so we should set that here before passing it to the serialzier and getting error
        request.data["creator"]=request.user.id
        return super().create(request, *args, **kwargs)
    
class UpdateDiscountAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            discount_percentage=int(request.data["discount"])
            if discount_percentage>100 or discount_percentage<0:
                return Response({"error":"discount has to be between 0 to 100"},status=status.HTTP_400_BAD_REQUEST)
            # Update all courses with the new discount percentage
            courses.objects.update(discount=discount_percentage)
            
            return Response({"message": f"All courses updated with discount: {discount_percentage}%"}, status=status.HTTP_200_OK)
        except (ValueError,KeyError):
            return Response({"error": "Invalid discount percentage"}, status=status.HTTP_400_BAD_REQUEST)
        

class retrieveDraftArticle(RetrieveAPIView):
    queryset=article.objects.all()
    serializer_class=articleSerializer
    permission_classes=[IsAdminUser]
    def get_object(self):
        # Extract 'href' from the URL path
        href = self.kwargs.get('href', None)
        if not href:
            raise ValueError("Expected 'href' in URL parameters")
        
        article_instance = get_object_or_404(article,href=href)
        return article_instance
    
class menuViewSet(viewsets.ModelViewSet):
    serializer_class=menuSerializer
    permission_classes=[IsAdminUser]
    def get_queryset(self):
        return menus.objects.all().select_related("parent")

    
class sessionViewSet(viewsets.ModelViewSet):
    queryset=session.objects.all()
    serializer_class=sessionSerializer
    permission_classes=[IsAdminUserOrReadOnly]
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return simpleSessionSerialzier
        return super().get_serializer_class()
    
ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.flv']

class CreateSessionView(APIView):
    permission_classes=[IsAdminUser]
    def post(self, request, course_id, format=None):
        try:
            course_instance = courses.objects.get(id=course_id)
            request.data["course"]=course_instance.id
            # Extract the file name from the request
            file_name = request.FILES.get('video').name
            
            # Validate the file extension
            _, file_extension = os.path.splitext(file_name)
            if file_extension.lower() not in ALLOWED_VIDEO_EXTENSIONS:
                return Response({'error': 'Invalid file type. Only video files are allowed.'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = sessionSerializer(data=request.data)
            if serializer.is_valid():
                session = serializer.save()
                return Response(sessionSerializer(session).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except courses.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)


class getRelatedCourses(ListAPIView):
    serializer_class=AllCourseSerializer
    queryset=courses.objects.all()
    def list(self, request, *args, **kwargs):
        course_instance=get_object_or_404(courses,href=kwargs["href"])
        queryset = courses.objects.filter(categoryID=course_instance.categoryID).exclude(href=kwargs["href"])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class contactViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAdminUser]
    queryset=contact.objects.all()
    serializer_class=contactSerializer
    
    #getRelatedSession gonna be used for each course alongside courseinfo
class getRelatedSession(ListAPIView):
    serializer_class=sessionSerializer
    queryset=session.objects.all()
    def list(self, request, *args, **kwargs):
        course_instance=get_object_or_404(courses,href=kwargs["href"])
        queryset = session.objects.filter(course=course_instance.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    #getDetailSessions gonna be used after clicking on a session in clinet side
class getDetailSessions(APIView):
    def get(self,request,*args,**kwargs):
        course_instance=get_object_or_404(courses,href=kwargs["href"])
        queryset = session.objects.filter(course=course_instance.id)
        session_serializer=sessionSerializer(queryset,many=True)
        session_instance=get_object_or_404(session,id=kwargs["pk"])
        single_session_serializer=sessionSerializer(session_instance)
        respons_data = {
            "session":single_session_serializer.data,
            "sessions":session_serializer.data
        }
        return Response(respons_data,status=status.HTTP_200_OK)
    
class discountCodeCheck(APIView):
    def post(self,request,*args,**kwargs):
        off_instance=get_object_or_404(off,code=kwargs["code"])
        if off_instance.course_id != request.data.get("course"):
            return Response({"error":"something is wronge with the code"},status=status.HTTP_400_BAD_REQUEST)
        
        else:
            if off_instance.max == off_instance.uses:
                return Response({"error":"this code has reached to its maximum usage , so it is invalid"},status=status.HTTP_409_CONFLICT)
            
            else:
                off_instance.uses += 1 if off_instance.uses+1 <=off_instance.max else 0
                off_instance.save()
                return Response({"off_percent":off_instance.percent},status=status.HTTP_202_ACCEPTED)
            
class registerUser(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,*args,**kwargs):
        course_instance=get_object_or_404(courses , href=kwargs["href"])
        if request.data.get("price") is None:
            return Response({"error":"you have to provide price"},status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                course_user_instance=courseUser(course = course_instance , user = request.user,price=request.data.get("price"))
                course_user_instance.save()
                serializer = courseuserSerializer(course_user_instance)
                return Response(serializer.data , status=status.HTTP_200_OK)
            except:
                return Response({"error":"something went wronge or you have already enrolled in this course"},status=status.HTTP_402_PAYMENT_REQUIRED)
            
        
            
        
        
        
        
        

    
    
    

    
    

    
    
    
    
    



