from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(max_length=500, required=False)  # Add custom fields if necessary
    profile_pic = forms.ImageField(required=False)  # Add profile picture field if necessary

    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'profile_pic')  # Add your custom fields here
