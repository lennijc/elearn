from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
# Create your models here.


class likedItem(models.Model):
    like = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    content_type=models.ForeignKey(ContentType,models.CASCADE)
    object_id= models.PositiveIntegerField()
    content_object= GenericForeignKey()
    