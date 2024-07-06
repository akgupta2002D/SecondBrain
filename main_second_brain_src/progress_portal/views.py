from rest_framework import viewsets
from .models import LifeGoal
from .serializers import LifeGoalSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect


class LifeGoalViewSet(viewsets.ModelViewSet):
    queryset = LifeGoal.objects.all()
    serializer_class = LifeGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


def viewProgressPortal(request):
    return render(request, 'progress_portal/dashboard.html')


def progress_portal_view(request):
    if not request.user.is_authenticated:
        # Make sure to replace 'login_url' with the actual URL name for login
        return redirect('login')

    life_goals = LifeGoal.objects.filter(user=request.user).prefetch_related(
        'projects__todo_lists__todo_items__subtasks'
    )
    return render(request, 'progress_portal/dashboard.html', {'life_goals': life_goals})
