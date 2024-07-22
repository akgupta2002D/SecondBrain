from django.db.models import Sum
from .models import Exam, ExamAttempt, UserAnswer, Question
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from .models import Class, Subject, Topic, Exam
# Create your views here.


@login_required
def view_exam_dashboard(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    topics = Topic.objects.all()
    exams = Exam.objects.filter(is_active=True)
    available_exams = Exam.objects.filter(is_active=True)
    user_attempts = ExamAttempt.objects.filter(
        user=request.user).select_related('exam')

    context = {
        'classes': classes,
        'subjects': subjects,
        'topics': topics,
        'exams': exams,
        'available_exams': available_exams,
        'user_attempts': user_attempts,
    }
    return render(request, "exam_quest/user_dashboard.html", context)


@login_required
def exam_and_result_dashboard(request):
    available_exams = Exam.objects.filter(is_active=True)
    user_attempts = ExamAttempt.objects.filter(
        user=request.user).select_related('exam')

    context = {
        'available_exams': available_exams,
        'user_attempts': user_attempts,
    }

    return render(request, "exam_quest/exam_dashboard.html", context)


@login_required
def exam_view(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)

    # Check if there's an ongoing attempt
    ongoing_attempt = ExamAttempt.objects.filter(
        user=request.user,
        exam=exam,
        is_completed=False
    ).first()

    if ongoing_attempt:
        # Resume the ongoing attempt
        questions = exam.questions.all().order_by('examquestion__order')
        return render(request, 'exam_quest/take_exam.html', {
            'exam': exam,
            'questions': questions,
            'attempt': ongoing_attempt
        })

    if request.method == 'POST':
        # Start a new attempt
        attempt = ExamAttempt.objects.create(
            user=request.user,
            exam=exam
        )
        questions = exam.questions.all().order_by('examquestion__order')
        return render(request, 'exam_quest/take_exam.html', {
            'exam': exam,
            'questions': questions,
            'attempt': attempt
        })

    return render(request, 'exam_quest/exam_start.html', {'exam': exam})


@login_required
def submit_exam(request, exam_id):
    if request.method == 'POST':
        exam = get_object_or_404(Exam, pk=exam_id)
        attempt = get_object_or_404(
            ExamAttempt, user=request.user, exam=exam, is_completed=False)

        for question in exam.questions.all():
            answer = request.POST.get(f'question_{question.id}')

            user_answer = UserAnswer.objects.create(
                attempt=attempt,
                question=question
            )

            if question.question_type in ['MCQ', 'IMG']:
                user_answer.selected_choice = answer

            elif question.question_type == 'TF':
                user_answer.true_false_answer = answer == 'True'
            elif question.question_type == 'FIB':
                user_answer.fill_blanks_answer = answer
            else:
                user_answer.text_answer = answer

            # Automatically grade MCQ, IMG, and TF questions
            if question.question_type in ['MCQ', 'IMG', 'TF']:
                user_answer.is_correct = (
                    (question.question_type in ['MCQ', 'IMG'] and answer == question.correct_choice) or
                    (question.question_type == 'TF' and (
                        answer == 'True') == question.is_true)
                )
                user_answer.points_earned = question.points if user_answer.is_correct else 0

            user_answer.save()

        attempt.end_time = timezone.now()
        attempt.is_completed = True
        attempt.score = UserAnswer.objects.filter(attempt=attempt, is_correct=True).aggregate(
            Sum('points_earned'))['points_earned__sum'] or 0
        attempt.save()

        return redirect('exam_result', attempt_id=attempt.id)

    return redirect('exam_view', exam_id=exam_id)


@login_required
def exam_result(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, pk=attempt_id, user=request.user)
    user_answers = UserAnswer.objects.filter(
        attempt=attempt).select_related('question')

    # Recalculate the score
    total_questions = user_answers.count()
    correct_answers = user_answers.filter(is_correct=True).count()

    attempt.score = correct_answers
    attempt.save()

    total_points = attempt.exam.questions.aggregate(Sum('points'))[
        'points__sum'] or 0
    percentage_score = (correct_answers / total_questions) * \
        100 if total_questions > 0 else 0
    passed = percentage_score >= attempt.exam.pass_percentage

    context = {
        'attempt': attempt,
        'user_answers': user_answers,
        'percentage_score': percentage_score,
        'passed': passed,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
    }

    return render(request, 'exam_quest/exam_result.html', context)
