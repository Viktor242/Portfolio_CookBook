from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)
    avatar = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2", "avatar", "bio")


class UserUpdateForm(UserChangeForm):
    password = None  # скрываем пароль в форме
    email = forms.EmailField(required=False)
    avatar = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "avatar", "bio")