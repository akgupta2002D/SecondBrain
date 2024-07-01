from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


class CustomUser(AbstractUser):
    """
    Custom user model extending the default AbstractUser model.

    """

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

    def __str__(self):
        """
        Return a string representation of the CustomUser instance.

        Returns:
            str: String representation of the user in the format 'firstname-role-username'.
        """
        return f'{self.firstname}-{self.role}-{self.username}'

    def is_family(self):
        """
        Check if the user has the family role.

        Returns:
            bool: True if the user is in the family role, False otherwise.
        """
        return self.role == self.FAMILY

    def is_friends(self):
        """
        Check if the user has the friends role.

        Returns:
            bool: True if the user is in the friends role, False otherwise.
        """
        return self.role == self.FRIENDS

    def is_acquaintance(self):
        """
        Check if the user has the acquaintance role.

        Returns:
            bool: True if the user is in the acquaintance role, False otherwise.
        """
        return self.role == self.ACQUAINTANCE


class InvitationKey(models.Model):
    """
    Model representing an invitation key.

    Attributes:
        key (str): The unique invitation key.
        is_used (bool): Indicates whether the key has been used.
    """
    key = models.CharField(max_length=50, unique=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        """
        Return a string representation of the InvitationKey instance.

        Returns:
            str: The invitation key.
        """
        return self.key


class Profile(models.Model):
    """
    Model representing a user profile.

    Attributes:
        user (CustomUser): One-to-one relationship with the CustomUser model.
        image (ImageField): Profile image, defaulting to 'default.png'.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png',
                              upload_to='profile_pictures')

    def __str__(self):
        """
        Return a string representation of the Profile instance.

        Returns:
            str: String representation of the profile in the format 'username Profile'.
        """
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """
        Override the save method to resize the profile image if it exceeds 300x300 pixels.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
