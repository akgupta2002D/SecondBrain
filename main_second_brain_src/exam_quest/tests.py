from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from custom_auth.models import CustomUser
from .models import Class, Subject, Topic, Question, Exam, ExamQuestion, ExamAttempt, UserAnswer


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

        # Create a multiple choice question
        self.mcq_question = Question.objects.create(
            text='What is 2 + 2?',
            topic=self.topic,
            difficulty='E',
            question_type='MCQ',
            points=1,
            choice_a='3',
            choice_b='4',
            choice_c='5',
            choice_d='6',
            correct_choice='B'
        )

        # Create an image choice question
        self.img_question = Question.objects.create(
            text='Which image shows a cat?',
            topic=self.topic,
            difficulty='E',
            question_type='IMG',
            points=1,
            correct_choice='A'
        )
        self.img_question.choice_a_image = SimpleUploadedFile(
            "cat.jpg", b"file_content")
        self.img_question.choice_b_image = SimpleUploadedFile(
            "dog.jpg", b"file_content")
        self.img_question.save()

        # Create a fill-in-the-blanks question
        self.fib_question = Question.objects.create(
            text='The capital of France is ___.',
            topic=self.topic,
            difficulty='E',
            question_type='FIB',
            points=1,
            blanks_answer='The capital of France is _Paris_.'
        )

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
            exam=self.exam, question=self.mcq_question, order=1)

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
        self.assertEqual(self.mcq_question.text, 'What is 2 + 2?')
        self.assertEqual(self.mcq_question.difficulty, 'E')
        self.assertEqual(self.mcq_question.question_type, 'MCQ')
        self.assertEqual(self.mcq_question.correct_choice, 'B')

    def test_exam_creation(self):
        self.assertEqual(self.exam.title, 'Math Midterm')
        self.assertEqual(self.exam.duration, 60)
        self.assertEqual(self.exam.pass_percentage, 60)

    def test_exam_question_relation(self):
        self.assertEqual(self.exam.questions.count(), 1)
        self.assertEqual(self.exam.questions.first(), self.mcq_question)

    def test_exam_attempt(self):
        attempt = ExamAttempt.objects.create(exam=self.exam, user=self.user)
        self.assertIsNone(attempt.end_time)
        self.assertFalse(attempt.is_completed)

    def test_user_answer_mcq(self):
        attempt = ExamAttempt.objects.create(exam=self.exam, user=self.user)
        user_answer = UserAnswer.objects.create(
            attempt=attempt,
            question=self.mcq_question,
            selected_choice='B'
        )
        self.assertEqual(user_answer.selected_choice,
                         self.mcq_question.correct_choice)

    def test_short_answer_question(self):
        short_answer_q = Question.objects.create(
            text='What is the capital of France?',
            topic=self.topic,
            difficulty='E',
            question_type='SA',
            points=1
        )

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
            question=self.mcq_question,
            selected_choice='B'
        )

        # Simulate exam completion
        attempt.is_completed = True
        attempt.score = 100.0  # Assuming full score for one correct answer
        attempt.save()

        self.assertTrue(attempt.is_completed)
        self.assertEqual(attempt.score, 100.0)

    def test_has_image_choices(self):
        self.assertTrue(self.img_question.has_image_choices())
        self.assertFalse(self.mcq_question.has_image_choices())

    def test_clean_method_image_choice(self):
        invalid_img_question = Question(
            text='Invalid image question',
            topic=self.topic,
            difficulty='E',
            question_type='IMG',
            points=1
        )
        with self.assertRaises(ValidationError):
            invalid_img_question.clean()

        invalid_img_question.choice_a_image = SimpleUploadedFile(
            "image_a.jpg", b"file_content")
        invalid_img_question.correct_choice = 'A'
        invalid_img_question.clean()  # Should not raise ValidationError

    def test_get_correct_answer_mcq(self):
        self.assertEqual(self.mcq_question.get_correct_answer(), '4')

    def test_get_correct_answer_img(self):
        self.assertEqual(self.img_question.get_correct_answer(),
                         self.img_question.choice_a_image)

    def test_get_correct_answer_tf(self):
        tf_question = Question.objects.create(
            text='Is Python a programming language?',
            topic=self.topic,
            difficulty='E',
            question_type='TF',
            points=1,
            is_true=True
        )
        self.assertEqual(tf_question.get_correct_answer(), 'True')

    def test_get_correct_answer_fib(self):
        self.assertEqual(self.fib_question.get_correct_answer(),
                         'The capital of France is Paris.')

    def test_user_answer_clean_method_mcq(self):
        attempt = ExamAttempt.objects.create(exam=self.exam, user=self.user)
        user_answer = UserAnswer(attempt=attempt, question=self.mcq_question)

        with self.assertRaises(ValidationError):
            user_answer.clean()

        user_answer.selected_choice = 'A'
        user_answer.clean()  # Should not raise ValidationError

    def test_user_answer_clean_method_img(self):
        attempt = ExamAttempt.objects.create(exam=self.exam, user=self.user)
        user_answer = UserAnswer(attempt=attempt, question=self.img_question)

        with self.assertRaises(ValidationError):
            user_answer.clean()

        user_answer.selected_choice = 'A'
        user_answer.clean()  # Should not raise ValidationError

    def test_user_answer_clean_method_fib(self):
        attempt = ExamAttempt.objects.create(exam=self.exam, user=self.user)
        user_answer = UserAnswer(attempt=attempt, question=self.fib_question)

        with self.assertRaises(ValidationError):
            user_answer.clean()

        user_answer.fill_blanks_answer = 'The capital of France is Paris.'
        user_answer.clean()  # Should not raise ValidationError

    def test_user_answer_clean_method_sa_la(self):
        for q_type in ['SA', 'LA']:
            question = Question.objects.create(
                text=f'Test {q_type} question',
                topic=self.topic,
                difficulty='E',
                question_type=q_type,
                points=1
            )
            attempt = ExamAttempt.objects.create(
                exam=self.exam, user=self.user)
            user_answer = UserAnswer(attempt=attempt, question=question)

            with self.assertRaises(ValidationError):
                user_answer.clean()

            user_answer.text_answer = 'Test answer'
            user_answer.clean()  # Should not raise ValidationError
