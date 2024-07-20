from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .forms import QuestionForm
from .models import Question


@require_http_methods(["GET", "POST"])
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save()
            return JsonResponse({
                'success': True,
                'question': question_to_dict(question)
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = QuestionForm()
    return render(request, 'exam_quest/create_questions.html', {'form': form})


@require_http_methods(["GET"])
def question_list(request):
    questions = Question.objects.all().order_by('-created_at')
    questions_data = [question_to_dict(question) for question in questions]
    return JsonResponse({'questions': questions_data})


def question_to_dict(question):
    return {
        'id': question.id,
        'text': question.text,
        'topic': question.topic.name,
        'difficulty': question.get_difficulty_display(),
        'question_type': question.get_question_type_display(),
        'points': question.points,
        'image': question.image.url if question.image else None,
        'choice_a': question.choice_a,
        'choice_b': question.choice_b,
        'choice_c': question.choice_c,
        'choice_d': question.choice_d,
        'choice_a_image': question.choice_a_image.url if question.choice_a_image else None,
        'choice_b_image': question.choice_b_image.url if question.choice_b_image else None,
        'choice_c_image': question.choice_c_image.url if question.choice_c_image else None,
        'choice_d_image': question.choice_d_image.url if question.choice_d_image else None,
        'correct_choice': question.correct_choice,
        'is_true': question.is_true,
        'blanks_answer': question.blanks_answer,
        'explanation': question.explanation,
        'hint': question.hint,
        'is_active': question.is_active,
        'created_at': question.created_at.isoformat(),
        'updated_at': question.updated_at.isoformat(),
    }
