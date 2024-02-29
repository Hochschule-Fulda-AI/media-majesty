from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from items.models import Item


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["username", "email"]


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "w-full py-2 px-4 rounded"}),
        required=True,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "w-full py-2 px-4 rounded"}),
        required=True,
    )


@login_required
def index(request):
    items = Item.objects.filter(created_by=request.user).all
    return render(request, "dashboard/index.html", {"items": items})


@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        password_form = ChangePasswordForm(request.POST)

        if user_form.is_valid() and password_form.is_valid():
            user = user_form.save(commit=False)
            if password_form.cleaned_data["password"]:
                user.set_password(password_form.cleaned_data["password"])
            user.save()

            print("User information updated successfully!")
            return redirect("dashboard:edit_profile")
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        password_form = ChangePasswordForm()

    return render(
        request,
        "dashboard/index.html",
        {"user_form": user_form, "password_form": password_form},
    )


@login_required
def delete_account(request):
    if request.method == "POST":
        request.user.delete()
        return redirect("/")
    return render(request, "dashboard/delete_account.html")
