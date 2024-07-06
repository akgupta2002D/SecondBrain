from rest_framework.routers import DefaultRouter
from .views import LifeGoalViewSet,  get_all_life_goals, viewProgressPortal
from django.urls import path, include

router = DefaultRouter()
router.register(r'life-goals', LifeGoalViewSet)

urlpatterns = [
    # Traditional Django views

    # DRF API URLs
    path('lifegoal/', include(router.urls)),
    path('view/', viewProgressPortal, name='portal_dashboard'),
    path('api/life_goals/', get_all_life_goals, name='get_all_life_goals'),
]
