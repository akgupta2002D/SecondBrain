from django.contrib import admin
from .models import Class, Subject, Topic, Question, Exam, ExamQuestion, ExamAttempt, UserAnswer


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_level')
    search_fields = ('name', 'class_level__name')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')
    search_fields = ('name', 'subject__name')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'truncated_text', 'topic', 'difficulty',
                    'question_type', 'points', 'is_active')
    list_filter = ('difficulty', 'question_type',
                   'is_active', 'topic__subject__class_level')
    search_fields = ('text', 'topic__name', 'topic__subject__name')
    fieldsets = (
        (None, {
            'fields': ('text', 'topic', 'difficulty', 'question_type', 'points', 'is_active', 'image', 'explanation', 'hint')
        }),
        ('Multiple Choice', {
            'fields': ('choice_a', 'choice_b', 'choice_c', 'choice_d', 'correct_choice'),
            'classes': ('collapse',),
        }),
        ('True/False', {
            'fields': ('is_true',),
            'classes': ('collapse',),
        }),
        ('Fill in the Blanks', {
            'fields': ('blanks_answer',),
            'classes': ('collapse',),
        }),
    )

    def truncated_text(self, obj):
        return (obj.text[:40] + '...') if len(obj.text) > 50 else obj.text

    truncated_text.short_description = 'Text'


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'class_level', 'subject',
                    'created_by', 'duration', 'pass_percentage', 'is_active')
    list_filter = ('class_level', 'subject', 'is_active')
    search_fields = ('title', 'class_level__name',
                     'subject__name', 'created_by__username')


@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'question', 'order')
    list_filter = ('exam__title',)
    search_fields = ('exam__title', 'question__text')


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('exam', 'user', 'start_time',
                    'end_time', 'score', 'is_completed')
    list_filter = ('exam__title', 'user__username', 'is_completed')
    search_fields = ('exam__title', 'user__username')


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'get_answer',
                    'is_correct', 'points_earned')
    list_filter = ('attempt__exam__title',
                   'attempt__user__username', 'is_correct')
    search_fields = ('attempt__exam__title',
                     'attempt__user__username', 'question__text')

    def get_answer(self, obj):
        if obj.question.question_type == 'MCQ':
            return obj.selected_choice
        elif obj.question.question_type == 'TF':
            return 'True' if obj.true_false_answer else 'False'
        elif obj.question.question_type == 'FIB':
            return obj.fill_blanks_answer
        else:
            return obj.text_answer
    get_answer.short_description = 'Answer'
