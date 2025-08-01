# Generated by Django 5.0.3 on 2024-07-12 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0038_alter_comment_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='status',
            field=models.CharField(choices=[('presell', 'presell'), ('start', 'start')], default='start', max_length=12),
        ),
        migrations.AlterField(
            model_name='courses',
            name='isComplete',
            field=models.BooleanField(default=False),
        ),
    ]
