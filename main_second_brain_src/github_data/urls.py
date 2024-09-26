from django.urls import path
from .views import fetch_github_data, fetch_spotify_data

urlpatterns = [
    path('github/', fetch_github_data, name='fetch_github_data'),
    path('spotify/', fetch_spotify_data, name='fetch_spotify_data'),
]
