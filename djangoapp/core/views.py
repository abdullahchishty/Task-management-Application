from rest_framework import generics,status
from .models import User,UserMessage
from .serializers import UserCreateSerializer,UserSerializer,UserUpdateSerializer,UserProfileSerializer,ChangePasswordSerializer,UserMessageSerializer,UserEmailSerializer
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login,logout
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse
from rest_framework import generics
from taskmanager.models import TaskInfo
from taskmanager.serializers import TaskInfoSerializer
from .permissions import IsOwnerOrAdmin,IsAdminUser
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail,mail_admins,BadHeaderError,EmailMessage
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import authentication
from dns import resolver
from dns.exception import DNSException
from rest_framework.response import Response
from rest_framework import status,permissions
import secrets
from django.shortcuts import get_object_or_404
import random
import time


#api of user create
class UserCreateViewSet(generics.CreateAPIView):
    queryset = User.objects.all() 
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        usernamee=request.data.get('username')
        emaill=request.data.get('email')
        exist_username=User.objects.filter(username=usernamee)
        exist_email=User.objects.filter(email=emaill)
        if exist_username:
            response_data={
                'status':'username is already exist'
            }
            return Response(response_data,status=status.HTTP_400_BAD_REQUEST)
        if exist_email:
            response_data={
                'status':'email is already exist'
            }
            return Response(response_data,status=status.HTTP_400_BAD_REQUEST)
        return super().post(request, *args, **kwargs)

'''
Pass username and password for to login
'''

@api_view(['POST'])
@permission_classes([])
def login_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Maintain the session

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            # print(user.id)
            response_data = {
                'token': access_token,
                'user_id': user.id,
                'status':'Successfully login',
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

#api of update user
class UpdateUserViewSet(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes=[IsOwnerOrAdmin]

    #get user by id and check user is owner or not
    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_id = self.kwargs['pk']
        if user_id != user.id:
            raise PermissionDenied("You do not have permission to update a user.")
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    #update user
    def put(self, request, *args, **kwargs):
        user = self.request.user
        user_id = self.kwargs['pk']
        if user_id != user.id:
            raise PermissionDenied("You do not have permission to update a user.")
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#api for to get user
class GetUserViewSet(generics.RetrieveAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[IsOwnerOrAdmin]
    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_id = self.kwargs['pk']
        if user_id != user.id:
            raise PermissionDenied("You do not have permission to update a user.")
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
#api for to get user profile 
class GetUserProfileViewSet(generics.RetrieveAPIView):
    queryset=User.objects.all()
    serializer_class=UserProfileSerializer
    permission_classes=[IsOwnerOrAdmin]
    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_id = self.kwargs['pk']
        if user_id != user.id:
            raise PermissionDenied("You do not have permission to update a user.")
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

#api of update user profile
class UpdateUserProfileViewSet(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes=[IsOwnerOrAdmin]
    
    #get user profile
    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_id = self.kwargs['pk']
        if user_id != user.id:
            raise PermissionDenied("You do not have permission to update a user profile.")
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    #update user profile
    def put(self, request, *args, **kwargs):
        user = self.request.user
        user_id = self.kwargs['pk']
        if user_id != user.id:
            raise PermissionDenied("You do not have permission to update a user profile.")
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status':'Successfully updated',
            }
            return Response(response_data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#api of change password
class ChangePasswordApiViewSet(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes=[IsOwnerOrAdmin]
    serializer_class = ChangePasswordSerializer
    
    #change password function
    def put(self, request, *args, **kwargs):
        user = self.request.user
        user_id = self.kwargs['pk']
        if user_id != user.id:
            raise PermissionDenied("You do not have permission to change a password.")
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status':'Successfully change password',
            }
            return Response(response_data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# class SendMail(generics.CreateAPIView):
#     queryset = UserMessage.objects.all()
#     serializer_class = UserEmailSerializer  # Use the UserEmailSerializer

#     def perform_create(self, serializer):
#         user_id = self.kwargs['id']
#         admin_user = get_object_or_404(User, pk=user_id)

#         if not admin_user.is_superuser:
#             return Response({'status': False, 'message': 'User is not an admin.'})

#         recipient_emails = serializer.validated_data['user_emails']  # Get selected recipient emails

#         if not recipient_emails:
#             return Response({'status': False, 'message': 'No recipient emails provided'})

#         email_subject = serializer.validated_data['subject']
#         email_message = serializer.validated_data['message']

#         # Send the email to selected recipients
#         email = EmailMessage(
#             email_subject,
#             email_message,
#             settings.EMAIL_HOST_USER,
#             recipient_emails
#         )
#         email.send(fail_silently=False)

#         # Save a UserMessage instance for each recipient
#         for email_address in recipient_emails:
#             recipient_user = User.objects.get(email=email_address)
#             user_message = UserMessage(
#                 user=recipient_user,
#                 subject=email_subject,
#                 message=email_message,
#                 recieving_user_email=email_address  # Save the selected email
#             )
#             user_message.save()

#         return Response({'status': True, 'message': 'Email sent successfully to selected users'})

# class SendMail(APIView):
#     permission_classes=[IsAdmin]
#     def post(self, request, user_id):
        
#         try:
#             user = UserMessage.objects.filter(user_id=user_id)
#         except UserMessage.DoesNotExist:
#             return Response({'status': False, 'message': 'User not found'})

#         email_subject = request.data.get('subject', 'Default Subject')
#         email_message = request.data.get('message', 'Default Message')
#         email=request.data['too']
#         emailw = EmailMessage(
#             email_subject,
#             email_message,
#             settings.EMAIL_HOST_USER,
#             [email]
#         )
        
#         emailw.send(fail_silently=False)

        
#         user.email_message = email_message
#         # user.save()

#         return Response({'status': True, 'message': 'Email sent successfully'})
    

class EmailConfirmationView(APIView): 
    def post(self, request):
        serializer = UserEmailSerializer(data=request.data)

        if serializer.is_valid():
            email = request.data.get('email')

            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            confirmation_code = ''.join(str(random.randint(0, 9)) for _ in range(8))

            confirmation_link = f"{confirmation_code}"

            subject = "Confirmation Email"
            message = f"Enter this code in verification form: {confirmation_link}"
            from_email = settings.EMAIL_HOST_USER

            send_mail(subject, message, from_email, [email])
            
            response_data={
                'confirmation_token':confirmation_code
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    


    









        


