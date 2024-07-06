from rest_framework.routers import DefaultRouter
from .views import get_all_life_goals, viewProgressPortal, life_goal_detail, project_detail
from django.urls import path, include
from .class_views import LifeGoalViewSet

# Initialize the default router and register the LifeGoalViewSet
router = DefaultRouter()
router.register(r'life-goals', LifeGoalViewSet)

# Define URL patterns for the application
urlpatterns = [
    # Traditional Django views
    path('view/', viewProgressPortal, name='portal_dashboard'),

    # DRF API URLs
    path('lifegoal/', include(router.urls)),
    path('api/life_goals/', get_all_life_goals, name='get_all_life_goals'),
    path('life_goal/<int:pk>/', life_goal_detail, name='life_goal_detail'),
    path('projects/<int:pk>/', project_detail, name='project_detail'),
]

"""
URL Configuration for Life Goals and Projects

The `urlpatterns` list routes URLs to views. For more information, please see:
https://docs.djangoproject.com/en/stable/topics/http/urls/

Routes:
    - /view/: Routes to the viewProgressPortal view.
    - /lifegoal/: Includes all routes registered with the DefaultRouter for the LifeGoalViewSet.
    - /api/life_goals/: Routes to the get_all_life_goals view.
    - /life_goal/<int:pk>/: Routes to the life_goal_detail view for a specific life goal.
    - /projects/<int:pk>/: Routes to the project_detail view for a specific project.
"""
