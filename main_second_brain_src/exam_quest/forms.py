from django import forms
from .models import Question, Topic


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'topic', 'difficulty', 'question_type', 'points', 'image',
                  'choice_a', 'choice_b', 'choice_c', 'choice_d',
                  'choice_a_image', 'choice_b_image', 'choice_c_image', 'choice_d_image',
                  'correct_choice', 'is_true', 'blanks_answer', 'explanation', 'hint']

    def clean(self):
        cleaned_data = super().clean()
        question_type = cleaned_data.get('question_type')

        if question_type in ['MCQ', 'IMG']:
            self.validate_multiple_choice(cleaned_data)
        elif question_type == 'TF':
            self.validate_true_false(cleaned_data)
        elif question_type == 'FIB':
            self.validate_fill_in_blanks(cleaned_data)

        return cleaned_data

    def validate_multiple_choice(self, cleaned_data):
        choices = [cleaned_data.get(f'choice_{c}') for c in 'abcd']
        choice_images = [cleaned_data.get(f'choice_{c}_image') for c in 'abcd']

        if self.cleaned_data['question_type'] == 'MCQ' and not any(choices):
            raise forms.ValidationError(
                "At least one choice must be provided for multiple choice questions.")

        if self.cleaned_data['question_type'] == 'IMG' and not any(choice_images):
            raise forms.ValidationError(
                "At least one image choice must be provided for image choice questions.")

        if not cleaned_data.get('correct_choice'):
            raise forms.ValidationError("A correct choice must be selected.")

    def validate_true_false(self, cleaned_data):
        if cleaned_data.get('is_true') is None:
            raise forms.ValidationError("Please select True or False.")

    def validate_fill_in_blanks(self, cleaned_data):
        blanks_answer = cleaned_data.get('blanks_answer')
        if not blanks_answer or '_' not in blanks_answer:
            raise forms.ValidationError(
                "Fill in the blanks answer must contain at least one blank (underscore).")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.all()

        # Make all fields not required initially
        for field in self.fields:
            self.fields[field].required = False

        # Make basic fields required
        required_fields = ['text', 'topic',
                           'difficulty', 'question_type', 'points']
        for field in required_fields:
            self.fields[field].required = True
