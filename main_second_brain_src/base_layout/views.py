from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def home(request):
    context = {
        "name": "Ankit"
    }
    return render(request, "base_layout/home.html", context)
