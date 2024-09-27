from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from PIL import Image
# Groups can be created to specify various permission to different types of users.
from django.utils import timezone


class CustomUser(AbstractUser):
    STUDENT = 'student'
    TEACHER = 'teacher'

    ROLE_CHOICES = (
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
    )
    # Add custom fields
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(unique=True, null=True, blank=True)
    phonenumber = models.CharField(max_length=15, null=True, blank=True)
    school_unique_id = models.CharField(max_length=50, unique=True, null=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    # Additional fields specific to each role
    # Additional fields and methods

    def __str__(self):
        return f'{self.firstname}-{self.school_unique_id}'

    def is_admin(self):
        return self.role == self.ADMIN

    def is_sub_admin(self):
        return self.role == self.SUB_ADMIN

    def is_student(self):
        return self.role == self.STUDENT

    def is_teacher(self):
        return self.role == self.TEACHER


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()  # This would run anyways.

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
