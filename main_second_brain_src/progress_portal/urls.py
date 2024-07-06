from rest_framework.routers import DefaultRouter
from .views import LifeGoalViewSet,  get_all_life_goals, viewProgressPortal, life_goal_detail, project_detail
from django.urls import path, include


router = DefaultRouter()
router.register(r'life-goals', LifeGoalViewSet)

urlpatterns = [
    # Traditional Django views

    # DRF API URLs
    path('lifegoal/', include(router.urls)),
    path('view/', viewProgressPortal, name='portal_dashboard'),
    path('api/life_goals/', get_all_life_goals, name='get_all_life_goals'),
    path('life_goal/<int:pk>/', life_goal_detail, name='life_goal_detail'),
    path('projects/<int:pk>/', project_detail, name='project_detail'),
]
