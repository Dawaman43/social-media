# Importing necessary Django modules
from django.db import models  # Import models from Django
from django.conf import settings  # To get the AUTH_USER_MODEL dynamically
from django.contrib.auth import get_user_model  # To fetch the user model
from django.urls import reverse  # For generating URLs for views
from django.db.models import F, Count  # To use specific query functions

# Get the User model (custom or default)
User = get_user_model()

# Profile model to store user profile details
class Profile(models.Model):
    # A one-to-one relationship with the User model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Profile picture with a default image if not set
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='images/default_profile.jpg')
    
    # Optional biography for the user
    bio = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        # String representation of the profile
        return f"{self.user.username}'s Profile"
    
    def get_profile_picture(self):
        # Returns the URL of the profile picture or default if not set
        return self.profile_picture.url if self.profile_picture else 'images/default_profile.jpg'


# UserPost model to represent posts made by users
class UserPost(models.Model):
    # Foreign key to link the post to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    # The content of the post
    post_text = models.TextField()
    
    # Automatically set the date and time when the post is created
    post_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        # Returns the URL to view the specific post
        return reverse('post_detail', kwargs={'pk': self.pk})

    # The following commented-out methods can be used to dynamically calculate like, comment, and share counts:
    # @property
    # def like_count(self):
    #     return self.likes.count()  # Dynamic calculation of like count

    # @property
    # def comment_count(self):
    #     return self.comments.count()  # Dynamic calculation of comment count

    # @property
    # def share_count(self):
    #     return self.shares.count()  # Dynamic calculation of share count


# Like model to represent user likes on posts
class Like(models.Model):
    # Foreign key to link the like to a user and a post
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, related_name='likes', on_delete=models.CASCADE)
    
    # Timestamp for when the like is created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Ensure a user can like a post only once
    class Meta:
        unique_together = ('user', 'post') 

    def __str__(self):
        # String representation of a like
        return f"{self.user} liked {self.post}"

# Comment model to represent user comments on posts
class Comment(models.Model):
    # Foreign key to link the comment to a user and a post
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name="comments")
    
    # Content of the comment
    content = models.TextField()
    
    # Automatically set the timestamp when the comment is created
    timestamp = models.DateTimeField(auto_now_add=True)

# Share model to represent user shares of posts
class Share(models.Model):
    # Foreign key to link the share to a user and a post
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, related_name='shares', on_delete=models.CASCADE)
    
    # Timestamp for when the post is shared
    share_date = models.DateTimeField(auto_now_add=True)

    # Ensure a user can share a post only once
    class Meta:
        unique_together = ('user', 'post') 

    def __str__(self):
        # String representation of a share
        return f"Share by {self.user} on {self.share_date}"
