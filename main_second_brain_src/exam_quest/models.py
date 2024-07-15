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
    """
    Represents a question under a specific topic.

    """
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
    ]

    text = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
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
    hint = models.TextField(
        blank=True, help_text="Hint for the question")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Question {self.id}: {self.text[:50]}..."


class Answer(models.Model):
    """
    Represents an answer to a specific question.

    """
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"Answer for Question {self.question.id}: {self.text[:50]}..."


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
    """
    Represents an answer provided by a user for a specific question in an exam attempt.

    """
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, null=True, blank=True)
    # For short and long answer questions
    text_answer = models.TextField(blank=True)
    is_correct = models.BooleanField(null=True)  # Null for ungraded answers
    points_earned = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Answer by {self.attempt.user} for Question {self.question.id}"
