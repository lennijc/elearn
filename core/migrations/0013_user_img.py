# Generated by Django 5.0.3 on 2024-06-05 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
