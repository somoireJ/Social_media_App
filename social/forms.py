from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, PasswordResetForm, SetPasswordForm, AuthenticationForm
)
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import Profile, Post, Comment
from .models import User as SocialUser  # Import the custom User model


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = SocialUser  # Update the model reference
        fields = ('username', 'email', 'password1', 'password2')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'website', 'location', 'profile_picture')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', 'image', 'video')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email address',
    }))


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = SocialUser  # Update the model reference
        fields = ('username', 'password')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'website', 'location', 'profile_picture')