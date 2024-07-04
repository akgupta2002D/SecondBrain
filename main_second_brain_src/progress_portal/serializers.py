from rest_framework import serializers
from .models import LifeGoal


class LifeGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeGoal
        fields = ['id', 'title', 'description', 'user']
