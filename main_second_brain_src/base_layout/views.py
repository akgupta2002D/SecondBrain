from django.shortcuts import render
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def home(request):
    app_list = [
        {'url_name': 'portal_dashboard',
            'icon_path': 'base_layout/images/progress_portal_image.png', 'name': 'Progress Portal'},
        {'url_name': 'upload_and_view',
            'icon_path': 'base_layout/images/scan_notes.jpg', 'name': 'Extract Notes'},
        {'url_name': 'exam_result_dashboard',
            'icon_path': 'base_layout/images/exam_prep_image.jpeg', 'name': 'Exam Prep'},
        {'url_name': 'fetch_github_data',
            'icon_path': 'base_layout/images/coming_soon.png', 'name': 'Socials Dashboard (Work in Progress!)'},
        {'url_name': 'homepage',
            'icon_path': 'base_layout/images/coming_soon1.png', 'name': 'Health Tracker (Coming Soon!)'}
    ]

    context = {
        'app_list': app_list,
    }
    return render(request, "base_layout/home.html", context)


def landingpage(request):
    user = request.user
    context = {
        "user": user
    }
    return render(request, "base_layout/landingpage.html", context)


def sphinx_docs(request):
    return render(request, 'docs/index.html')
