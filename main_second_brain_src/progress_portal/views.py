from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import LifeGoal
from .serializers import LifeGoalSerializer
from rest_framework.permissions import IsAuthenticated


class LifeGoalViewSet(viewsets.ModelViewSet):
    queryset = LifeGoal.objects.all()
    serializer_class = LifeGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensuring users see only their own life goals
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user to the current user on creation
        serializer.save(user=self.request.user)
