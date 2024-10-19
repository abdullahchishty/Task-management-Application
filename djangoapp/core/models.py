from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# User Model
class User(AbstractUser):
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=11)
    bio=models.TextField(blank=True)
    interest=models.CharField(max_length=225,blank=True)
    image=models.ImageField(upload_to='store/images', blank=True, null=True)
    

class UserMessage(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    subject=models.CharField(max_length=225)
    message=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    recieving_user_email=models.EmailField(unique=False,default=None)


class EmailComposition(models.Model):
    recipients = models.ManyToManyField(User)
    subject = models.CharField(max_length=100)
    message_content = models.TextField()

    def __str__(self):
        return self.subject