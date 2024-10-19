from django.contrib import admin
from . import models

#admin can handle task through this decorator
@admin.register(models.TaskInfo)
class TaskInfoAdmin(admin.ModelAdmin):
    list_display=['title','description','due_date','priority','category','location','status']