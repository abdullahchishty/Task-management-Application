# Generated by Django 4.2.5 on 2023-10-09 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(default='store/images/profile.jpg', upload_to='store/images'),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
