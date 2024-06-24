from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


class CustomUser(AbstractUser):
    FAMILY = 'family'
    FRIENDS = 'friends'
    ACQUAINTANCE = 'acquaintance'

    ROLE_CHOICES = (
        (FAMILY, 'Family'),
        (FRIENDS, 'Friends'),
        (ACQUAINTANCE, 'Acquaintance')
    )

    # Add custom fields
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(unique=True, null=True, blank=True)
    phonenumber = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default=FAMILY)

    # Additional fields specific to each role
    # Additional fields and methods

    def __str__(self):
        return f'{self.firstname}-{self.role}'

    def is_family(self):
        return self.role == self.FAMILY

    def is_friends(self):
        return self.role == self.FRIENDS

    def is_acquaintance(self):
        return self.role == self.ACQUAINTANCE


class InvitationKey(models.Model):
    key = models.CharField(max_length=50, unique=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.key


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png',
                              upload_to='profile_pictures')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()  # This would run anyways.

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
