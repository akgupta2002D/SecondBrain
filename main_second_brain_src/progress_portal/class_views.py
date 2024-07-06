from asgiref.sync import sync_to_async
from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import LifeGoal, Project, ToDoItem
from .serializers import LifeGoalSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .utils import get_all_life_goals_sync, get_projects_for_life_goal_sync


class LifeGoalViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing LifeGoal instances.

    Attributes:
        queryset: A queryset of all LifeGoal objects.
        serializer_class: The serializer class for LifeGoal.
        permission_classes: Permissions required to access this viewset.

    Methods:
        get_queryset: Returns a filtered queryset of LifeGoal objects for the authenticated user.
    """
    queryset = LifeGoal.objects.all()
    serializer_class = LifeGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns a queryset of LifeGoal objects filtered by the authenticated user.

        Returns:
            QuerySet: A filtered queryset of LifeGoal objects.
        """
        return self.queryset.filter(user=self.request.user)
