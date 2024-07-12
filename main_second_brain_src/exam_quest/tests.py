from django.test import TestCase
from django.core.exceptions import ValidationError
from custom_auth.models import CustomUser
from .models import Class, Subject, Topic, Question, Answer, Exam, ExamQuestion, ExamAttempt, UserAnswer


class ExamPlatformModelTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = CustomUser.objects.create_user(
            username='testuser', password='12345')

        # Create a class
        self.class_obj = Class.objects.create(
            name='Grade 10', description='Tenth grade')

        # Create a subject
        self.subject = Subject.objects.create(
            name='Mathematics', class_level=self.class_obj)

        # Create a topic
        self.topic = Topic.objects.create(name='Algebra', subject=self.subject)

        # Create a question
        self.question = Question.objects.create(
            text='What is 2 + 2?',
            topic=self.topic,
            difficulty='E',
            question_type='MCQ',
            points=1
        )

        # Create answers for the question
        self.correct_answer = Answer.objects.create(
            question=self.question, text='4', is_correct=True)
        self.wrong_answer = Answer.objects.create(
            question=self.question, text='5', is_correct=False)

        # Create an exam
        self.exam = Exam.objects.create(
            title='Math Midterm',
            description='Midterm exam for Grade 10 Math',
            class_level=self.class_obj,
            subject=self.subject,
            created_by=self.user,
            duration=60,
            pass_percentage=60
        )

        # Add question to exam
        ExamQuestion.objects.create(
            exam=self.exam, question=self.question, order=1)

    def test_class_creation(self):
        self.assertEqual(self.class_obj.name, 'Grade 10')
        self.assertEqual(str(self.class_obj), 'Grade 10')

    def test_subject_creation(self):
        self.assertEqual(self.subject.name, 'Mathematics')
        self.assertEqual(str(self.subject), 'Mathematics - Grade 10')

    def test_topic_creation(self):
        self.assertEqual(self.topic.name, 'Algebra')
        self.assertEqual(str(self.topic), 'Algebra - Mathematics - Grade 10')

    def test_question_creation(self):
        self.assertEqual(self.question.text, 'What is 2 + 2?')
        self.assertEqual(self.question.difficulty, 'E')
        self.assertEqual(self.question.question_type, 'MCQ')

    def test_answer_creation(self):
        self.assertTrue(self.correct_answer.is_correct)
        self.assertFalse(self.wrong_answer.is_correct)

    def test_exam_creation(self):
        self.assertEqual(self.exam.title, 'Math Midterm')
        self.assertEqual(self.exam.duration, 60)
        self.assertEqual(self.exam.pass_percentage, 60)

    def test_exam_question_relation(self):
        self.assertEqual(self.exam.questions.count(), 1)
        self.assertEqual(self.exam.questions.first(), self.question)

    def test_exam_attempt(self):
        attempt = ExamAttempt.objects.create(exam=self.exam, user=self.user)
        self.assertIsNone(attempt.end_time)
        self.assertFalse(attempt.is_completed)

    def test_user_answer(self):
        attempt = ExamAttempt.objects.create(exam=self.exam, user=self.user)
        user_answer = UserAnswer.objects.create(
            attempt=attempt,
            question=self.question,
            selected_answer=self.correct_answer
        )
        self.assertTrue(user_answer.selected_answer.is_correct)

    # def test_invalid_pass_percentage(self):
    #     with self.assertRaises(ValidationError):
    #         Exam.objects.create(
    #             title='Invalid Exam',
    #             class_level=self.class_obj,
    #             subject=self.subject,
    #             created_by=self.user,
    #             pass_percentage=101  # Invalid percentage
    #         )

    def test_mcq_question(self):
        attempt = ExamAttempt.objects.create(exam=self.exam, user=self.user)
        user_answer = UserAnswer.objects.create(
            attempt=attempt,
            question=self.question,
            selected_answer=self.correct_answer
        )
        self.assertTrue(user_answer.selected_answer.is_correct)

        user_answer_wrong = UserAnswer.objects.create(
            attempt=attempt,
            question=self.question,
            selected_answer=self.wrong_answer
        )
        self.assertFalse(user_answer_wrong.is_correct)

    def test_short_answer_question(self):
        short_answer_q = Question.objects.create(
            text='What is the capital of France?',
            topic=self.topic,
            difficulty='E',
            question_type='SA',
            points=1
        )
        Answer.objects.create(question=short_answer_q,
                              text='Paris', is_correct=True)

        attempt = ExamAttempt.objects.create(exam=self.exam, user=self.user)
        user_answer = UserAnswer.objects.create(
            attempt=attempt,
            question=short_answer_q,
            text_answer='Paris'
        )
        # Initially, short answer questions are not automatically graded
        self.assertIsNone(user_answer.is_correct)

        # Simulate manual grading
        user_answer.is_correct = True
        user_answer.save()
        self.assertTrue(user_answer.is_correct)

    def test_exam_completion(self):
        attempt = ExamAttempt.objects.create(exam=self.exam, user=self.user)
        UserAnswer.objects.create(
            attempt=attempt,
            question=self.question,
            selected_answer=self.correct_answer
        )

        # Simulate exam completion
        attempt.is_completed = True
        attempt.score = 100.0  # Assuming full score for one correct answer
        attempt.save()

        self.assertTrue(attempt.is_completed)
        self.assertEqual(attempt.score, 100.0)
