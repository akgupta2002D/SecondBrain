from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LifeGoalViewSet

router = DefaultRouter()
router.register(r'lifegoals', LifeGoalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
