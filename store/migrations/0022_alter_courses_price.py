# Generated by Django 5.0.3 on 2024-06-09 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_alter_article_href_alter_courses_href'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
