from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.shortcuts import redirect, render
from items.models import Category, Item

from .forms import SignUpForm


def index(request):
    items = Item.objects.order_by("-created_at").filter(
        is_sold=False, is_approved=True
    )[0:6]
    categories = Category.objects.all()
    return render(
        request, "core/index.html", {"categories": categories, "items": items}
    )


def contact(request):
    return render(request, "core/contact.html")


def about(request):
    return render(request, "core/about.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            print("valid")
            form.save()
            return redirect("/login")
    else:
        form = SignUpForm()
    return render(request, "core/signup.html", {"form": form})


@login_required
def logout(request):
    auth_logout(request)
    return redirect("/")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        return redirect("core:confirm_email", email=email)
    return render(request, "core/forgot_password.html")


def confirm_email(request, email):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            try:
                user = User.objects.get(email=email)
                if len(new_password) < 8:
                    messages.error(
                        request,
                        "Password is too short. It must contain at least 8 characters.",
                    )
                elif new_password.isdigit():
                    messages.error(request, "Password cannot be entirely numeric.")
                else:
                    try:
                        validate_password(new_password, user=user)
                    except DjangoValidationError as e:
                        messages.error(request, e.messages[0])
                    else:
                        user.set_password(new_password)
                        user.save()
                        messages.success(
                            request, "Password reset successful. You can log in now."
                        )
            except User.DoesNotExist:
                messages.error(request, "User with this email does not exist.")

    return render(request, "core/confirm_email.html", {"email": email})
