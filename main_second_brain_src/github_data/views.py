import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


def fetch_github_data(request):
    # GitHub API Setup
    headers = {
        'Authorization': f'token {settings.GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }
    username = '{username}'  # Replace with your GitHub username
    repos_url = f'https://api.github.com/users/akgupta2002D/repos'
    commits_url = f'https://api.github.com/repos/akgupta2002D/SecondBrain/commits'

    # Fetch GitHub Data
    repos_response = requests.get(repos_url, headers=headers)
    if repos_response.status_code != 200:
        return HttpResponse('Error fetching GitHub repositories.', status=repos_response.status_code)

    repos = repos_response.json()
    num_repos = len(repos)

    # Get latest commit data for the first repository
    latest_commit_info = {}
    if repos:
        first_repo = repos[0]['name']
        commits_response = requests.get(commits_url.format(
            repo_name=first_repo), headers=headers)
        if commits_response.status_code == 200:
            latest_commit_info = commits_response.json()[0]

    best_repos = sorted(
        repos, key=lambda x: x['stargazers_count'], reverse=True)[:3]

    return render(request, 'github_data/github_dashboard.html', {
        'num_repos': num_repos,
        'latest_commit': latest_commit_info,
        'best_repos': best_repos,
    })


def fetch_spotify_data(request):
    # Spotify API Setup
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope="user-top-read"
    ))

    # Fetch Spotify Data
    spotify_top_tracks = []
    try:
        spotify_results = sp.current_user_top_tracks(limit=5)
        spotify_top_tracks = spotify_results['items']
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    # Format data for JSON response
    top_tracks = [
        {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album_image': track['album']['images'][0]['url'],
            'preview_url': track['preview_url']
        }
        for track in spotify_top_tracks
    ]

    return JsonResponse({'top_tracks': top_tracks})
