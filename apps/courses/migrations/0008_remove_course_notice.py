# Generated by Django 2.2 on 2020-09-08 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20200908_1337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='notice',
        ),
    ]
