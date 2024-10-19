from django.urls import path,include
from django.contrib.auth.decorators import login_required 
from . import views

urlpatterns = [
    path('register/', views.UserCreateViewSet.as_view(), name='user-register'),                                #create a new user
    path('login/', views.login_view, name='login'),                                                            #login user
    path('update/<int:pk>/',views.UpdateUserViewSet.as_view(),name='user-update'),                             #update user through id
    path('getuser/<int:pk>/',views.GetUserViewSet.as_view(),name='get-user'),                                  #get user by id
    path('userprofile/<int:pk>/',views.GetUserProfileViewSet.as_view(),name='profile-image'),                  #get user profile through id
    path('updatepfp/<int:pk>',views.UpdateUserProfileViewSet.as_view(),name='update-user-profile'),            #update profile picture
    path('changepassword/<int:pk>/',views.ChangePasswordApiViewSet.as_view(), name='user_change_password'),    #change password through user id
    path('email-confirmation/', views.EmailConfirmationView.as_view(), name='email_confirmation'),
]
