from django.contrib import admin
from .models import Class, Subject, Topic, Question, Answer, Exam, ExamQuestion, ExamAttempt, UserAnswer


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
    list_display = ('text', 'topic', 'difficulty',
                    'question_type', 'points', 'is_active')
    list_filter = ('difficulty', 'question_type',
                   'is_active', 'topic__subject__class_level')
    search_fields = ('text', 'topic__name', 'topic__subject__name')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')
    search_fields = ('text', 'question__text')


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
    list_filter = ('exam__title', 'question__text')
    search_fields = ('exam__title', 'question__text')


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('exam', 'user', 'start_time',
                    'end_time', 'score', 'is_completed')
    list_filter = ('exam__title', 'user__username', 'is_completed')
    search_fields = ('exam__title', 'user__username')


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_answer',
                    'is_correct', 'points_earned')
    list_filter = ('attempt__exam__title',
                   'attempt__user__username', 'is_correct')
    search_fields = ('attempt__exam__title',
                     'attempt__user__username', 'question__text')
