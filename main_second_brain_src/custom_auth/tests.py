from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import CustomUser


class CustomUserModelTest(TestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username='john',
            email='john@example.com',
            password='testpass123',
            firstname='John',
            lastname='Doe',
            phonenumber='1234567890',
            date_of_birth='2000-01-01',
            role=CustomUser.FAMILY
        )

    def test_create_user(self):
        self.assertEqual(self.user1.username, 'john')
        self.assertEqual(self.user1.email, 'john@example.com')
        self.assertTrue(self.user1.check_password('testpass123'))
        self.assertEqual(self.user1.firstname, 'John')
        self.assertEqual(self.user1.lastname, 'Doe')
        self.assertEqual(self.user1.phonenumber, '1234567890')
        self.assertIsNotNone(self.user1.date_of_birth)
        self.assertEqual(self.user1.role, CustomUser.FAMILY)

    def test_string_representation(self):
        self.assertEqual(str(self.user1), 'John-family-john')

    def test_user_roles(self):
        self.assertTrue(self.user1.is_family())
        self.assertFalse(self.user1.is_friends())
        self.assertFalse(self.user1.is_acquaintance())

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_user_validation(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                username='',
                email='invalid@example.com',
                password='testpass123'
            )
