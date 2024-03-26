from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your username",
                "class": "w-full p-2 my-2 border border-gray-300 rounded-sm",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Your password",
                "class": "w-full p-2 my-2 border border-gray-300 rounded-sm",
            }
        )
    )


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your username",
                "class": "w-full p-2 my-2 border border-gray-300 rounded-sm",
            }
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Your email address",
                "class": "w-full p-2 my-2 border border-gray-300 rounded-sm",
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Your password",
                "class": "w-full p-2 my-2 border border-gray-300 rounded-sm",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repeat password",
                "class": "w-full p-2 my-2 border border-gray-300 rounded-sm",
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("hs-fulda.de"):
            raise ValidationError(
                "Only users with hs-fulda.de domain are allowed to register."
            )
        return email
