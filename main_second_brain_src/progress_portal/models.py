"""
Models for Life Goals, Projects, ToDoItems, and SubTasks

This module defines the models for managing life goals, projects, to-do items, and subtasks. Each model is connected through foreign key relationships to represent a hierarchical structure.

Classes:
    LifeGoal
    Project
    ToDoItem
    SubTask
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class LifeGoal(models.Model):
    """
    Represents a life goal set by a user.

    Attributes:
        title (str): The title of the life goal.
        description (str): A detailed description of the life goal.
        icon (FileField): An optional icon representing the life goal.
        user (ForeignKey): The user who set the life goal.
    """
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    icon = models.FileField(
        upload_to='icons/', default='icons/default_icon.svg', blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='life_goals')

    def __str__(self):
        return self.title


class Project(models.Model):
    """
    Represents a project associated with a life goal.

    Attributes:
        title (str): The title of the project.
        description (str): A detailed description of the project.
        image (ImageField): An optional image representing the project.
        life_goal (ForeignKey): The life goal associated with the project.
        state (str): The current state of the project (planning, in progress, closed).
    """
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
    """
    Represents a to-do item within a project.

    Attributes:
        title (str): The title of the to-do item.
        description (str): A detailed description of the to-do item.
        due_date (date): The due date for the to-do item.
        priority (int): The priority level of the to-do item (1: Low, 2: Medium, 3: High).
        todo_list (ForeignKey): The project to which the to-do item belongs.
        files (FileField): Optional files associated with the to-do item.
        completed (bool): Indicates whether the to-do item is completed.
    """
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
    """
    Represents a subtask within a to-do item.

    Attributes:
        title (str): The title of the subtask.
        description (str): A detailed description of the subtask.
        due_date (date): The due date for the subtask.
        status (bool): Indicates whether the subtask is completed.
        todo_item (ForeignKey): The to-do item to which the subtask belongs.
    """
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.BooleanField(default=False)
    todo_item = models.ForeignKey(
        ToDoItem, on_delete=models.CASCADE, related_name='subtasks')

    def __str__(self):
        return self.title
