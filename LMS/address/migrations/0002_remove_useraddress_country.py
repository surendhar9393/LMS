# Generated by Django 3.0 on 2021-07-25 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraddress',
            name='country',
        ),
    ]