from django.urls import path
from . import views
from . import question_creation_views

urlpatterns = [
    path("dashboard/", views.view_exam_dashboard, name="exam_dashboard"),
    path("exam_result_dashboard/", views.exam_and_result_dashboard,
         name="exam_result_dashboard"),

    path('exam/<int:exam_id>/', views.exam_view, name='exam_view'),
    path('exam/<int:exam_id>/submit/', views.submit_exam, name='submit_exam'),
    path('exam/result/<int:attempt_id>/',
         views.exam_result, name='exam_result'),
    path('create-question/', question_creation_views.create_question,
         name='create_question'),
    path('questions/', question_creation_views.question_list, name='question_list'),
]
