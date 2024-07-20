from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.conf import settings


class Class(models.Model):
    """
    Represents a class level.

    """
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    """
    Represents a subject taught in a specific class level.

    """
    name = models.CharField(max_length=100)
    class_level = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.class_level}"


class Topic(models.Model):
    """
    Represents a topic under a specific subject.

    """
    name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
    ]
    QUESTION_TYPES = [
        ('MCQ', 'Multiple Choice'),
        ('TF', 'True/False'),
        ('FIB', 'Fill in the Blanks'),
        ('SA', 'Short Answer'),
        ('LA', 'Long Answer'),
        ('MAT', 'Matching'),
        ('IMG', 'Image Choice'),
    ]

    text = models.TextField()
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES)
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPES)
    image = models.ImageField(
        upload_to='question_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    points = models.PositiveIntegerField(default=1)
    time_limit = models.PositiveIntegerField(
        help_text="Time limit in seconds", null=True, blank=True)
    explanation = models.TextField(
        blank=True, help_text="Explanation for the correct answer")
    hint = models.TextField(blank=True, help_text="Hint for the question")
    is_active = models.BooleanField(default=True)

    # Multiple Choice fields
    choice_a = models.TextField(blank=True)
    choice_b = models.TextField(blank=True)
    choice_c = models.TextField(blank=True)
    choice_d = models.TextField(blank=True)
    choice_a_image = models.ImageField(
        upload_to='choice_images/', null=True, blank=True)
    choice_b_image = models.ImageField(
        upload_to='choice_images/', null=True, blank=True)
    choice_c_image = models.ImageField(
        upload_to='choice_images/', null=True, blank=True)
    choice_d_image = models.ImageField(
        upload_to='choice_images/', null=True, blank=True)

    correct_choice = models.CharField(max_length=1, choices=[(
        'A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], blank=True)

    # True/False field
    is_true = models.BooleanField(
        null=True, blank=True, help_text="For True/False questions")

    # Fill in the Blanks fields
    blanks_answer = models.TextField(
        blank=True, help_text="Correct answer for Fill in the Blanks questions. Use underscores to represent blanks, e.g., 'The capital of France is _Paris_.'")

    def __str__(self):
        return f"Question {self.id}: {self.text[:20]}..."

    def has_image_choices(self):
        return self.question_type == 'IMG' and any([self.choice_a_image, self.choice_b_image, self.choice_c_image, self.choice_d_image])

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.question_type in ['MCQ', 'IMG'] and not self.correct_choice:
            raise ValidationError(
                "Multiple Choice and Image Choice questions must have a correct choice specified.")
        elif self.question_type == 'MCQ' and not self.correct_choice:
            raise ValidationError(
                "Multiple Choice questions must have a correct choice specified.")

        elif self.question_type == 'TF' and self.is_true is None:
            raise ValidationError(
                "True/False questions must have the is_true field set.")
        elif self.question_type == 'FIB' and not self.blanks_answer:
            raise ValidationError(
                "Fill in the Blanks questions must have a blanks_answer specified.")


class Exam(models.Model):
    """
    Represents an exam.

    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    class_level = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, through='ExamQuestion')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_exams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration = models.PositiveIntegerField(
        help_text="Duration in minutes", null=True, blank=True)
    pass_percentage = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Passing percentage for the exam",
        default=60
    )
    is_active = models.BooleanField(default=True)
    shuffle_questions = models.BooleanField(default=False)
    show_result_immediately = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ExamQuestion(models.Model):
    """
    Represents the association between an exam and a question, with an order.

    """
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Question {self.order} in {self.exam}"


class ExamAttempt(models.Model):
    """
    Represents an attempt by a user to complete an exam.

    """
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Attempt by {self.user} on {self.exam}"


class UserAnswer(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    # Multiple Choice answer
    selected_choice = models.CharField(max_length=1, choices=[(
        'A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], blank=True)

    # True/False answer
    true_false_answer = models.BooleanField(null=True, blank=True)

    # Fill in the Blanks answer
    fill_blanks_answer = models.TextField(blank=True)

    # For short and long answer questions
    text_answer = models.TextField(blank=True)

    is_correct = models.BooleanField(null=True)  # Null for ungraded answers
    points_earned = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Answer by {self.attempt.user} for Question {self.question.id}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.question.question_type == 'MCQ' and not self.selected_choice:
            raise ValidationError(
                "Must select a choice for Multiple Choice questions.")
        elif self.question.question_type == 'TF' and self.true_false_answer is None:
            raise ValidationError(
                "Must provide a True/False answer for True/False questions.")
        elif self.question.question_type == 'FIB' and not self.fill_blanks_answer:
            raise ValidationError(
                "Must provide an answer for Fill in the Blanks questions.")
