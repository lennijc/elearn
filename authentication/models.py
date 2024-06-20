from django.db import models

# Create your models here.

class banUser(models.Model):
    phone=models.CharField(max_length=11)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.phone