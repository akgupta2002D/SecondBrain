"""
ViewSets and Async Views for Life Goals and Projects

This module provides the views and viewsets for managing life goals and projects. The views include both synchronous and asynchronous processing to handle requests efficiently.

Functions:
    viewProgressPortal:
    get_all_life_goals:
    life_goal_detail:
    project_detail:
"""

from asgiref.sync import sync_to_async
from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import LifeGoal, Project, ToDoItem
from .serializers import LifeGoalSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .utils import get_all_life_goals_sync, get_projects_for_life_goal_sync


def viewProgressPortal(request):
    """
    Renders the progress portal dashboard.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered dashboard page.
    """
    return render(request, 'progress_portal/dashboard.html')


async def get_all_life_goals(request):
    """
    Asynchronously retrieves all life goals with their associated projects.

    Args:
        request (HttpRequest): The request object.

    Returns:
        JsonResponse: A JSON response containing all life goals and their projects.
    """
    life_goals = await sync_to_async(list)(LifeGoal.objects.all())
    data = []
    for life_goal in life_goals:
        projects = await sync_to_async(list)(life_goal.projects.all())
        projects_data = [{"title": project.title,
                          "description": project.description,
                          "id": project.id} for project in projects]
        data.append({
            "life_goal": life_goal.title,
            "icon": life_goal.icon.url if life_goal.icon else None,
            "projects": projects_data,
            "id": life_goal.id,
        })
    return JsonResponse(data, safe=False)


async def life_goal_detail(request, pk):
    """
    Asynchronously retrieves details of a specific life goal.

    Args:
        request (HttpRequest): The request object.
        pk (int): The primary key of the life goal.

    Returns:
        JsonResponse: A JSON response containing the life goal details and associated projects.
    """
    try:
        life_goal = await sync_to_async(LifeGoal.objects.get)(pk=pk)
    except LifeGoal.DoesNotExist:
        return JsonResponse({'error': 'Life goal not found'}, status=404)

    projects = await sync_to_async(list)(life_goal.projects.all())
    projects_data = [{"title": project.title, "description": project.description if project.description else None,
                      "id": project.id} for project in projects]
    data = {
        "life_goal": life_goal.title,
        "icon": life_goal.icon.url if life_goal.icon else None,
        "projects": projects_data,
        "id": life_goal.id,
        "description": life_goal.description if life_goal.description else None,
    }
    return JsonResponse(data)


async def project_detail(request, pk):
    """
    Asynchronously retrieves details of a specific project.

    Args:
        request (HttpRequest): The request object.
        pk (int): The primary key of the project.

    Returns:
        JsonResponse: A JSON response containing the project details and associated to-do items.
    """
    try:
        project = await sync_to_async(Project.objects.get)(pk=pk)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)

    todo_items = await sync_to_async(list)(project.todo_items.all())
    todo_items_data = [
        {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "due_date": item.due_date,
            "priority": item.get_priority_display(),
            "completed": item.completed,
            "files": item.files.url if item.files else None
        }
        for item in todo_items
    ]
    data = {
        "title": project.title,
        "description": project.description if project.description else None,
        "id": project.id,
        "todo_items": todo_items_data
    }
    return JsonResponse(data)
