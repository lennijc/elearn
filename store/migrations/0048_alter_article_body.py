# Generated by Django 5.0.3 on 2024-07-20 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0047_alter_article_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='body',
            field=models.TextField(),
        ),
    ]
