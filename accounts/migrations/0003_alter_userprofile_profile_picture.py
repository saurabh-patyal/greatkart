# Generated by Django 3.2.6 on 2021-08-16 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default.svg', null=True, upload_to='userprofile'),
        ),
    ]
