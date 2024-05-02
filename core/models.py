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
    phone_number=models.CharField(max_length=11)
    ROLE_CHOICES=[
    ('U',"USER"),
    ('A',"ADMIN")
    ]
    role = models.CharField(max_length=1,choices=ROLE_CHOICES,default="U")
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    
    


