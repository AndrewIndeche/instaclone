# Generated by Django 3.2.8 on 2021-10-25 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0005_auto_20211025_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='alaska.jpg', upload_to='images/'),
        ),
    ]
