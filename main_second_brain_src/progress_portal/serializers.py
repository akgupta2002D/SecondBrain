from rest_framework import serializers
from .models import LifeGoal


class LifeGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeGoal
        fields = ['id', 'title', 'description', 'user']
        # Ensure user field is not required from API input
        read_only_fields = ('user',)

    def create(self, validated_data):
        # Add the user from the request context directly to the model instance
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
