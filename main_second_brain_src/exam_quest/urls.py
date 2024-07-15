from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.view_exam_dashboard, name="exam_dashboard"),
]
