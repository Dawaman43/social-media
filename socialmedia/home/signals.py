# Import necessary modules from Django
from django.db.models.signals import post_save  # Signal that is triggered after saving an object
from django.dispatch import receiver  # Used to connect the signal to the receiver function
from .models import Profile  # Importing the Profile model from the current app
from django.contrib.auth import get_user_model  # Function to get the User model

# Get the User model, which might be custom or default
User = get_user_model()

# Signal receiver that is triggered after a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    This signal creates a Profile whenever a new user is created.
    `instance` refers to the user being saved, and `created` is a boolean that indicates 
    whether the user is newly created.
    """
    # If the user is newly created, create a corresponding Profile
    if created:
        Profile.objects.create(user=instance)

# Signal receiver that is triggered after a User is saved (whether new or updated)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    This signal ensures the Profile is saved when the User is saved.
    `instance` refers to the user whose profile should be saved.
    """
    # Save the profile associated with the user (if it exists)
    instance.profile.save()
