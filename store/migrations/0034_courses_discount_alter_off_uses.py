# Generated by Django 5.0.3 on 2024-07-11 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0033_off'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='discount',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='off',
            name='uses',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
