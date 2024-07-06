from asgiref.sync import sync_to_async
from django.shortcuts import render
from rest_framework import viewsets
from .models import LifeGoal, Project, ToDoItem
from .serializers import LifeGoalSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .utils import get_all_life_goals_sync, get_projects_for_life_goal_sync


class LifeGoalViewSet(viewsets.ModelViewSet):
    queryset = LifeGoal.objects.all()
    serializer_class = LifeGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


def viewProgressPortal(request):
    return render(request, 'progress_portal/dashboard.html')


# def progress_portal_view(request):
#     if not request.user.is_authenticated:
#         # Make sure to replace 'login_url' with the actual URL name for login
#         return redirect('login')

#     life_goals = LifeGoal.objects.filter(user=request.user).prefetch_related(
#         'projects__todo_items__subtasks'
#     )
#     return render(request, 'progress_portal/dashboard.html', {'life_goals': life_goals})


async def get_all_life_goals(request):
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


# Life Goal Detail response
async def life_goal_detail(request, pk):
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
    try:
        project = await sync_to_async(Project.objects.get)(pk=pk)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)

    todo_items = await sync_to_async(list)(project.todo_items.all())
    todo_items_data = [
        {
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
