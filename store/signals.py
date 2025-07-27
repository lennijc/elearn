import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from storages.backends.s3boto3 import S3Boto3Storage
from .models import LessonVideo
from django.conf import settings

@receiver(post_save, sender=LessonVideo)
def upload_default_image(sender, instance, created, **kwargs):
    print('here we are in the signals')
    # Only trigger on creation, not updates
    if created and not instance.video_file:
        # Define the default image file
        default_image_path = settings.DEFAULT_LESSON_IMAGE
        if not os.path.exists(default_image_path):
            return  # Skip if default image doesn't exist

        # Define the S3 path (same as upload_to in the model)
        s3_path = f'videos/{instance.lesson.title}_{instance.id}'

        # Upload the default image to S3
        storage = S3Boto3Storage()
        with open(default_image_path, 'rb') as file:
            storage.save(s3_path, file)

        # Update the instance's video_file field with the S3 path
        instance.video_file = s3_path
        instance.save()