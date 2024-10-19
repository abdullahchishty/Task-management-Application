from rest_framework import serializers
from .models import TaskInfo
from core.models import User

#get fields through taskinfo model for to create task
class TaskInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskInfo
        fields = ['id','title','description','due_date','priority','category','location','status']


# class TaskInfoUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=User
#         fields=['id','first_name','last_name','phone']


    
