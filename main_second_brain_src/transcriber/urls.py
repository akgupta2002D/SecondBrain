from django.urls import path
from . import views

urlpatterns = [
    path('transcribe/', views.transcribe, name='transcribe'),
    path('status/<int:transcription_id>/', views.get_status, name='get_status'),
]
