# Generated by Django 3.2.7 on 2021-09-24 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_students_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students',
            name='profile_pic',
        ),
    ]