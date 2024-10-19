from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer,UserCreateSerializer as BaseUserCreateSerializer
from .models import User,UserMessage
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password


# get fields through user model for to create task
class UserCreateSerializer(BaseUserCreateSerializer): 
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['username','password','email','first_name','last_name','phone','bio','interest']

# get fields through user model fro to display task
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['username', 'email', 'first_name', 'last_name','phone','bio','interest']

#get fields through user model for to update
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','phone']
    
#get field through user model for to get and update profile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['image']

#get password through user model for to update
class ChangePasswordSerializer(serializers.ModelSerializer):

    #field which is required
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    old_password = serializers.CharField(write_only=True, required=True)

    #pass fields
    class Meta:
        model = User
        fields = ('old_password', 'password')
    

    #validate old password
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    #update
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserMessage
        fields=['subject','message']

class UserEmailSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('emails',)
