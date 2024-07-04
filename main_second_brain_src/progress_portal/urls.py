from rest_framework.routers import DefaultRouter
from .views import LifeGoalViewSet

router = DefaultRouter()
router.register(r'life-goals', LifeGoalViewSet, basename='lifegoal')

urlpatterns = router.urls
