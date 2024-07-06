from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class LifeGoal(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(
        upload_to='icons/', default='icons/default_icon.png', blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='life_goals')

    def __str__(self):
        return self.title


class Project(models.Model):
    STATE_CHOICES = (
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    )
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='project_images/', blank=True, null=True)
    life_goal = models.ForeignKey(
        LifeGoal, on_delete=models.CASCADE, related_name='projects')
    state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        default='planning'
    )

    def __str__(self):
        return self.title


class ToDoItem(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    priority = models.IntegerField(
        choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2)
    todo_list = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='todo_items')
    files = models.FileField(
        upload_to='todo_item_files/', blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class SubTask(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.BooleanField(default=False)
    todo_item = models.ForeignKey(
        ToDoItem, on_delete=models.CASCADE, related_name='subtasks')

    def __str__(self):
        return self.title
