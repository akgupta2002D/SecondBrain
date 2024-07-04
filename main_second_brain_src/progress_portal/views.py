from rest_framework import viewsets
from .models import LifeGoal
from .serializers import LifeGoalSerializer
from rest_framework.permissions import IsAuthenticated


class LifeGoalViewSet(viewsets.ModelViewSet):
    queryset = LifeGoal.objects.all()
    serializer_class = LifeGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
