# Generated by Django 4.2 on 2023-05-15 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatApp', '0003_alter_profile_age_alter_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default='default_pic', max_length=1000, upload_to='profile_pic'),
        ),
    ]
