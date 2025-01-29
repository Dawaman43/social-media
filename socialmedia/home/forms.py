from django import forms
from .models import UserPost, Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']  # Profile-specific fields

    bio = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Write bio (maximum of 300 words)', 'class': 'form-control', 'rows': 5})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get user instance from kwargs
        super(ProfileForm, self).__init__(*args, **kwargs)

        if user:
            # Set initial values for first_name and last_name from the user model (optional)
            self.fields['first_name'] = forms.CharField(initial=user.first_name, required=False, max_length=30)
            self.fields['last_name'] = forms.CharField(initial=user.last_name, required=False, max_length=30)

    def save(self, commit=True):
        # Save the profile instance first
        profile = super().save(commit=False)

        # Update the user instance with the new first_name and last_name (if provided)
        user = profile.user
        if 'first_name' in self.cleaned_data:
            user.first_name = self.cleaned_data['first_name']
        if 'last_name' in self.cleaned_data:
            user.last_name = self.cleaned_data['last_name']
        user.save()  # Save the user instance

        # Save the profile instance if commit is True
        if commit:
            profile.save()

        return profile  # Return the saved profile

class PostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ['post_text']

class SearchForm(forms.Form):
    q = forms.CharField(label='Search Posts', max_length=100)
