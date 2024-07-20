from django.contrib import admin
from django.utils.html import format_html
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
        ('Answer Options', {
            'fields': ('choice_a', 'choice_b', 'choice_c', 'choice_d',
                       'choice_a_image', 'choice_b_image', 'choice_c_image', 'choice_d_image',
                       'correct_choice', 'is_true', 'blanks_answer'),
        }),
    )

    def truncated_text(self, obj):
        return (obj.text[:40] + '...') if len(obj.text) > 50 else obj.text
    truncated_text.short_description = 'Text'

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            answer_options = fieldsets[1][1]['fields']
            if obj.question_type == 'MCQ':
                fieldsets[1][1]['fields'] = [f for f in answer_options if f in (
                    'choice_a', 'choice_b', 'choice_c', 'choice_d', 'correct_choice')]
            elif obj.question_type == 'IMG':
                fieldsets[1][1]['fields'] = [f for f in answer_options if f in (
                    'choice_a_image', 'choice_b_image', 'choice_c_image', 'choice_d_image', 'correct_choice')]
            elif obj.question_type == 'TF':
                fieldsets[1][1]['fields'] = [
                    f for f in answer_options if f == 'is_true']
            elif obj.question_type == 'FIB':
                fieldsets[1][1]['fields'] = [
                    f for f in answer_options if f == 'blanks_answer']
            else:  # For SA and LA, no answer options are needed
                fieldsets = fieldsets[:1]
        return fieldsets

    readonly_fields = ['image_preview', 'choice_a_image_preview',
                       'choice_b_image_preview', 'choice_c_image_preview', 'choice_d_image_preview']

    def image_preview(self, obj):
        return self._get_image_preview(obj.image)

    def choice_a_image_preview(self, obj):
        return self._get_image_preview(obj.choice_a_image)

    def choice_b_image_preview(self, obj):
        return self._get_image_preview(obj.choice_b_image)

    def choice_c_image_preview(self, obj):
        return self._get_image_preview(obj.choice_c_image)

    def choice_d_image_preview(self, obj):
        return self._get_image_preview(obj.choice_d_image)

    def _get_image_preview(self, image):
        if image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', image.url)
        return "No image"


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
        if obj.question.question_type in ['MCQ', 'IMG']:
            return obj.selected_choice
        elif obj.question.question_type == 'TF':
            return 'True' if obj.true_false_answer else 'False'
        elif obj.question.question_type == 'FIB':
            return obj.fill_blanks_answer
        else:
            return obj.text_answer
    get_answer.short_description = 'Answer'
