from django.db import models
from django.conf import settings

#task info model
class TaskInfo(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title=models.CharField(max_length=225)
    description=models.TextField()
    due_date=models.DateField()
    priority=models.CharField(max_length=225)
    category=models.CharField(max_length=225)
    location=models.CharField(max_length=225,blank=True, null=True)
    status=models.BooleanField(default=False)

