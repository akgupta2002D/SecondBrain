from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Profile


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal receiver to create a profile whenever a new CustomUser is created.

    This function is called automatically after a CustomUser instance is saved. If the user instance
    is being created for the first time, a corresponding Profile instance is also created.

    Args:
        sender (type): The model class that sent the signal (CustomUser).
        instance (CustomUser): The instance of the CustomUser that was saved.
        created (bool): A boolean indicating whether a new record was created.
        **kwargs: Additional keyword arguments.

    """
    if created:
        Profile.objects.create(user=instance)
        print(f"Profile created for {instance.username}")


@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    """
    Signal receiver to save the profile whenever a CustomUser is saved.

    This function ensures that the corresponding Profile instance is saved whenever the CustomUser
    instance is saved.

    Args:
        sender (type): The model class that sent the signal (CustomUser).
        instance (CustomUser): The instance of the CustomUser that was saved.
        **kwargs: Additional keyword arguments.

    """
    instance.profile.save()
    print(f"Profile saved for {instance.username}")
