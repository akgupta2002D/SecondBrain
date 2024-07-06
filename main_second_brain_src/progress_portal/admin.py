from django.contrib import admin
from .models import LifeGoal, ToDoItem, ToDoList, SubTask, Project
# Register your models here.

admin.site.register(LifeGoal)
admin.site.register(ToDoItem)
admin.site.register(ToDoList)
admin.site.register(SubTask)
admin.site.register(Project)
