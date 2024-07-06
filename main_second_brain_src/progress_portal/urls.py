from rest_framework.routers import DefaultRouter
from .views import LifeGoalViewSet, progress_portal_view
from django.urls import path, include

router = DefaultRouter()
router.register(r'life-goals', LifeGoalViewSet)

urlpatterns = [
    # Traditional Django views

    # DRF API URLs
    path('lifegoal/', include(router.urls)),
    path('view/', progress_portal_view, name='life_goals_view')
]
