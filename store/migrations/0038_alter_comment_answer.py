# Generated by Django 5.0.3 on 2024-07-12 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0037_alter_comment_answer_alter_comment_isanswer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='answer',
            field=models.IntegerField(choices=[(0, 0), (1, 1)], default=0),
        ),
    ]
