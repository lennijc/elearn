from django.db import models
from django.contrib.auth.models import AbstractUser
# from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
from django.utils import timezone
import uuid


#get the role field base on the is_staff attribute of abstactUser to check if it is admin or normal user

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=255,null=True)
    ROLE_CHOICES=[
    ('USER',"user"),
    ('ADMIN',"admin")
    ]
    DEFAULT_ROLE_CHOICE='USER'
    role = models.CharField(max_length=5,choices=ROLE_CHOICES,default=DEFAULT_ROLE_CHOICE)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True)
    phone=models.CharField(max_length=11,null=True)
    img=models.ImageField(upload_to="uploads/",null=True,blank=True)
    email = models.EmailField(unique=True, error_messages={
        'unique': "A user with that email already exists.",
    })

class Order(models.Model):
    course=models.ForeignKey("store.courses",on_delete=models.PROTECT)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    price=models.PositiveIntegerField(default=0)
    def __str__(self):
        return  f"{self.course}"
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'user'], name='already ordered and registered'),
        ]
    
    
    


