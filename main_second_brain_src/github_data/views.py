
import requests
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


def fetch_github_data(request):
    # GitHub API Setup

    return render(request, 'github_data/github_dashboard.html', {
    })
