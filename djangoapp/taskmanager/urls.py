from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:user_id>/', views.CreateTaskView.as_view(),name='task-create'),                     #url for to create task through user id
    path('read/<int:pk>/<int:user_id>', views.GetTaskView.as_view(), name='task-read'),                   #url for to read task by task and user id
    path('update/<int:pk>/<int:user_id>', views.UpdateRetrieveTaskView.as_view(),name='task-update'),     #url for to update task through user ids and task id
    path('delete/<int:pk>/<int:user_id>', views.DeleteTaskView.as_view(),name='task-delete'),             #url for to delete task through user id and 
    path('completedtask/<int:user_id>/',views.CompletedTaskView.as_view(),name='completed-task-list'),    #url of completed task through user id
    path('incompletedtask/<int:user_id>/',views.InCompletedTaskView.as_view(),name='completed-task-list'),#url of incompleted task through user id
]
