# Generated by Django 5.0.3 on 2024-05-24 09:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_courseuser_courses_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('answer', models.IntegerField()),
                ('isAnswer', models.BooleanField()),
                ('score', models.CharField(choices=[('1', 'one'), ('2', 'two'), ('3', 'three'), ('4', 'four'), ('5', 'five')], max_length=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='courses',
            name='user',
        ),
        migrations.AddField(
            model_name='courses',
            name='price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='courses',
            name='student',
            field=models.ManyToManyField(related_name='student_user', through='store.courseUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='courseuser',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.courses'),
        ),
        migrations.AddConstraint(
            model_name='courseuser',
            constraint=models.UniqueConstraint(fields=('course', 'user'), name='cannot_register_twice'),
        ),
        migrations.AddField(
            model_name='comment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.courses'),
        ),
        migrations.AddField(
            model_name='comment',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
