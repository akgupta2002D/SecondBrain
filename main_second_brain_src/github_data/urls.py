from django.urls import path
from .views import fetch_github_data

urlpatterns = [
    path('github/', fetch_github_data, name='fetch_github_data'),
]
