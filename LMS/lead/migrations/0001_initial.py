# Generated by Django 3.0 on 2021-07-25 06:16

import LMS.lead.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Document name like Aadhar, PAN, Licence, etc..', max_length=64, unique=True, verbose_name='Document Type')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
            ],
        ),
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name of User')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text="Customer's primary mobile number e.g. +91{10 digit mobile number}", max_length=128, region=None, unique=True, verbose_name='Mobile Number')),
                ('status', models.CharField(choices=[('Fresh', 'Fresh'), ('Form Pending', 'Form Pending'), ('Document Pending', 'Document Pending'), ('Hot Application', 'TIER_3'), ('Approved', 'TIER_3'), ('Rejected', 'TIER_3'), ('Converted', 'TIER_3'), ('Closed', 'TIER_3')], default='Fresh', max_length=60, verbose_name='Status')),
                ('age', models.PositiveIntegerField(blank=True, null=True, verbose_name='Age')),
                ('occupation', models.CharField(blank=True, max_length=60, null=True, verbose_name='Status')),
                ('income', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Monthly Income')),
                ('source', models.CharField(choices=[('Fb', 'Fb'), ('WebSite', 'WebSite'), ('Google', 'Google')], default='Fresh', max_length=60, verbose_name='Status')),
                ('action_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='action_owner', to=settings.AUTH_USER_MODEL)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='address.UserAddress')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='address.City')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=256, upload_to=LMS.lead.models.generate_file_path)),
                ('number', models.CharField(default='----', help_text='Input the number from the file uploaded..', max_length=100, verbose_name='Document Number')),
                ('document_type', models.ForeignKey(help_text='Document type like Registration Certificate, Licence, etc..', on_delete=django.db.models.deletion.PROTECT, to='lead.DocumentType')),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lead.Lead')),
            ],
        ),
    ]
