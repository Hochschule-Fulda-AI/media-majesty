from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages
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
        email = request.POST.get('email')  # Get email from the form

        # Dummy notification that a reset link has been sent to the email
        messages.success(request, f"A password reset link has been sent to {email}")

        return render(request, 'core/forgot_password.html')
    return render(request, 'core/forgot_password.html')