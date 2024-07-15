from typing import Any, Dict
from rest_framework import serializers
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import password_validation, get_user_model
from ..models import menus,courses,categories,article,courseUser,comment,session,notification,contact,orderModel,off
from django.db.models import Avg
User = get_user_model()

class contactSerializer(serializers.ModelSerializer):
    class Meta:
        model=contact
        fields="__all__"

class simpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude=["password"]

class simpleCommentSerialzier(serializers.ModelSerializer):
    creator=simpleUserSerializer(read_only=True)
    class Meta:
        model=comment
        fields="__all__"
        
class simpleSessionSerialzier(serializers.ModelSerializer):
    course=serializers.SlugRelatedField(slug_field="name",read_only=True)
    class Meta:
        model=session
        fields="__all__"
class sessionSerializer(serializers.ModelSerializer):
    class Meta:
        model=session
        fields="__all__"

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = contact
        fields = ['name', 'email', 'phone',"body"]

class articleSerializer(serializers.ModelSerializer):
    creator=serializers.SlugRelatedField(read_only=True,slug_field="username")
    class Meta:
        model=article
        fields="__all__"
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation["category"]:
            representation["category"]=instance.category.title
        return representation

class simpleMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model =menus
        fields="__all__"
class menuSerializer(serializers.ModelSerializer):
    parent=serializers.SerializerMethodField()
    class Meta:
        model=menus
        fields="__all__"
    def get_parent(self,obj):
        if obj.parent:
            return obj.parent.title
        return None
class coursesSerializer(serializers.ModelSerializer):
    creator=serializers.StringRelatedField()
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
    
class notificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=notification
        fields="__all__"


        
class NavbarCategoriesSerializer(serializers.ModelSerializer):
    sub_menu=coursesSerializer(source="courses_set",many=True,read_only=True)
    class Meta:
        model=categories
        fields=["id","title","createdAt","updatedAt","name","sub_menu"]



class commentSerializer(serializers.ModelSerializer):
    creator=simpleUserSerializer(read_only=True)
    #mainCommentID=simpleCommentSerialzier(read_only=True)
    course=serializers.SlugRelatedField(slug_field="name",read_only=True)
    #answer content is the reverse of maincommentID because mainCommentID is refering to the question or mainComment
    #but answer content is refering to the answer or the reply comment to the mainComment
    answerContent=simpleCommentSerialzier(source="replies",many=True,read_only=True)
    class Meta:
        model=comment
        fields="__all__"
    def validate(self, data):
        """
        Check that either 'course' or 'article' is provided, but not both.
        """
        if data.get('course') and data.get('article'):
            raise serializers.ValidationError("Either 'course' or 'article' must be provided, but not both.")
        return data
    
class simpleCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=courses
        fields="__all__"
        
class answerCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=comment
        fields="__all__"
    def validate(self, data):
        """
        Check that either 'course' or 'article' is provided, but not both.
        """
        if data.get('course') and data.get('article'):
            raise serializers.ValidationError("Either 'course' or 'article' must be provided, but not both.")
        return data

# class sessionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=session
#         fields="__all__"


class AllCourseSerializer(serializers.ModelSerializer):
    creator=serializers.SlugRelatedField(read_only=True,slug_field="username")
    courseAverageScore=serializers.SerializerMethodField()
    registers=serializers.SerializerMethodField()
    class Meta:
        model=courses
        exclude=["student"]
    def get_courseAverageScore(self,obj):
        #for the average score we have to be fair and ignore the answer comments because the answer comment 
        #by default give score 5 to the course so thats why we filter the comment by the isAnswer=False
        average_score = comment.objects.filter(course=obj).filter(isAnswer=False).aggregate(Avg("score"))
        return int(average_score["score__avg"]) if average_score["score__avg"] else 5
    def get_registers(self,obj):
        courseStudentsCount=courseUser.objects.filter(course=obj).count()
        return courseStudentsCount
    
class UserSerializer(serializers.ModelSerializer):
    notifications = notificationSerializer(source="notification_set",many=True,read_only=True)
    courses = AllCourseSerializer(source="student_user",many=True)
    class Meta:
        model = User
        exclude = ['password'] #hashed password excluded

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if 'role' in validated_data:
            if validated_data['role'] == 'ADMIN':
                instance.is_staff = True
            else:
                instance.is_staff = False
        instance.save()

class AllArticleSerializer(serializers.ModelSerializer):
    creator=serializers.SlugRelatedField(read_only=True,slug_field="username")
    class Meta:
        model=article
        fields="__all__"

class articleInfoSerializer(serializers.ModelSerializer):
    category=categorySerializer(read_only=True)
    creator=UserSerializer(read_only=True)
    comments=commentSerializer(source="comment_set",many=True,read_only=True)
    class Meta:
        model=article
        fields="__all__"

class categorySubMenu(serializers.ModelSerializer):
    sub_menu=AllCourseSerializer(source="subMenu",many=True)
    class Meta:
        model=categories
        fields="__all__"

class courseInfoSerializer(serializers.ModelSerializer):
    categoryID=categorySerializer(read_only=True)
    creator=UserSerializer(read_only=True)
    # comments=commentSerializer(source="comment_set",many=True,read_only=True)
    #we have to send only the comments with isAnswer=0 because client wants it that way when showing the comments
    comments=serializers.SerializerMethodField()
    sessions=sessionSerializer(source="session_set",many=True,read_only=True)
    class Meta:
        model=courses
        exclude=["student"]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        context = self.context
        representation["courseStudentsCount"] = context["courseStudentsCount"]
        representation["isUserRegisteredToThisCourse"] = context["isUserRegisteredToThisCourse"]
        return representation
    
    def get_comments(self,obj):
        queryset=comment.objects.filter(course=obj).filter(isAnswer=False)
        serializer = commentSerializer(instance=queryset,many=True)
        return serializer.data

class courseuserSerializer(serializers.ModelSerializer):
    #student = coursesSerializer(source="student_user",many=True,read_only=True)
    #course=coursesSerializer(source="course_set",many=True)
    user=simpleUserSerializer(read_only=True)
    course=coursesSerializer(read_only=True)
    class Meta:
        model=courseUser
        fields="__all__"

class orderSerializer(serializers.ModelSerializer):
    course=AllCourseSerializer(read_only=True)
    class Meta:
        model=orderModel
        fields="__all__"


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    message = serializers.CharField(max_length=500)
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        """
        Check that the new password and its confirmation match.
        """
        if data['new_password']!= data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "The passwords do not match."})
        return data  


class userProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone','name')
        

class offSerializer(serializers.ModelSerializer):
    class Meta:
        model=off
        fields="__all__"

