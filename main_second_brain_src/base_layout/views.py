from django.shortcuts import render, HttpResponse

# Create your views here.


def home(request):
    context = {
        "name": "Ankit"
    }
    return render(request, "base_layout/home.html", context)
