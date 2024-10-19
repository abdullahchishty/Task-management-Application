from rest_framework import generics,status
from rest_framework.response import Response
from .models import TaskInfo
from .serializers import TaskInfoSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.urls import reverse
from . import permissions
from .permissions import IsOwnerOrAdmin
from django.core.exceptions import PermissionDenied
from core.models import User
from core.serializers import UserUpdateSerializer


#api of create task
class CreateTaskView(generics.CreateAPIView):
    queryset = TaskInfo.objects.all()
    serializer_class = TaskInfoSerializer
    permission_classes=[IsOwnerOrAdmin]

    #check user_id and then create
    def perform_create(self, serializer):
        user = self.request.user
        user_id = self.kwargs['user_id']
        if user_id != user.id:
            raise PermissionDenied("You do not have permission to create a task for another user.")
        serializer.save(user_id=user_id)  

  
#api for to get task
class GetTaskView(generics.RetrieveAPIView):
    queryset = TaskInfo.objects.all()
    serializer_class = TaskInfoSerializer
    permission_classes=[IsOwnerOrAdmin]

    #check id and then get task data
    def get_queryset(self):
        user=self.request.user
        user_id = self.kwargs['user_id']
        if user_id != user.id:
            raise PermissionDenied("You do not have permission to read a task for another user.")
        queryset = TaskInfo.objects.filter(user_id=user_id)
        return queryset
    
    
#api of get task info and update task
class UpdateRetrieveTaskView(generics.RetrieveUpdateAPIView):
    queryset = TaskInfo.objects.all()
    serializer_class = TaskInfoSerializer
    permission_classes=[IsOwnerOrAdmin]
    
    #get task
    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_id = self.kwargs['user_id']
        if user_id != user.id:
            raise PermissionDenied("You do not have permission to update a task for another user.")
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    #update task
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#api of delete task
class DeleteTaskView(generics.DestroyAPIView):
    queryset = TaskInfo.objects.all()
    serializer_class = TaskInfoSerializer
    permission_classes=[IsOwnerOrAdmin]

    #check id and then delete
    def get_queryset(self):
        user=self.request.user
        user_id = self.kwargs['user_id']
        if user_id != user.id:
            raise PermissionDenied("You do not have permission to delete a task for another user.")
        queryset = TaskInfo.objects.filter(user_id=user_id)
        print("Successfully deleted")
        return queryset


#api of completed task
class CompletedTaskView(generics.ListAPIView):
    queryset=TaskInfo.objects.all()
    serializer_class=TaskInfoSerializer
    
    #check user is valid and then get completed task
    def get_queryset(self):
        try:
            user = self.request.user
            user_id = self.kwargs['user_id']
            if user.id != user_id:
                raise PermissionDenied("You do not have permission to view a task for another user.")
            queryset = TaskInfo.objects.filter(user_id=user_id).filter(status=True)
            return queryset
        except TaskInfo.DoesNotExist:
            return Response({"detail": "TaskInfo not found"}, status=status.HTTP_404_NOT_FOUND)
        
#api of incompleted task
class InCompletedTaskView(generics.ListAPIView):
    queryset=TaskInfo.objects.all()
    serializer_class=TaskInfoSerializer

    #check user is valid and then get incpmpleted task
    def get_queryset(self):
        try:
            user = self.request.user
            user_id = self.kwargs['user_id']
            if user.id != user_id:
                raise PermissionDenied("You do not have permission to view a task for another user.")
            queryset = TaskInfo.objects.filter(user_id=user_id).filter(status=False)
            return queryset
        except TaskInfo.DoesNotExist:
            return Response({"detail": "TaskInfo not found"}, status=status.HTTP_404_NOT_FOUND)
        

