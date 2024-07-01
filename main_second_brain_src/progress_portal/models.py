from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class LifeGoal(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='life_goals')

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    image = models.ImageField(
        upload_to='project_images/', blank=True, null=True)
    life_goal = models.ForeignKey(
        LifeGoal, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.title


class ToDoList(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    priority = models.IntegerField(
        choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='todo_lists')
    files = models.FileField(
        upload_to='todo_list_files/', blank=True, null=True)

    def __str__(self):
        return self.title


class ToDoItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    priority = models.IntegerField(
        choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2)
    todo_list = models.ForeignKey(
        ToDoList, on_delete=models.CASCADE, related_name='todo_items')
    files = models.FileField(
        upload_to='todo_item_files/', blank=True, null=True)

    def __str__(self):
        return self.title


class SubTask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.BooleanField(default=False)
    todo_item = models.ForeignKey(
        ToDoItem, on_delete=models.CASCADE, related_name='subtasks')

    def __str__(self):
        return self.title
