from django.shortcuts import render
from .models import Class, Subject, Topic, Exam
# Create your views here.


def view_exam_dashboard(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    topics = Topic.objects.all()
    exams = Exam.objects.filter(is_active=True)

    context = {
        'classes': classes,
        'subjects': subjects,
        'topics': topics,
        'exams': exams,
    }
    return render(request, "exam_quest/user_dashboard.html", context)
