from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Your username",
            "class": "w-full p-2 my-2 border border-gray-300 rounded-sm"
            })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Your password",
            "class": "w-full p-2 my-2 border border-gray-300 rounded-sm"
            })
    )


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Your username",
            "class": "w-full p-2 my-2 border border-gray-300 rounded-sm"
            })
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Your email address",
            "class": "w-full p-2 my-2 border border-gray-300 rounded-sm"
            })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Your password",
            "class": "w-full p-2 my-2 border border-gray-300 rounded-sm"
            })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Repeat password",
            "class": "w-full p-2 my-2 border border-gray-300 rounded-sm"
            })
    )
