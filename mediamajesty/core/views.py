from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
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
        email = request.POST.get('email')
        return redirect('core:confirm_email', email=email)
    return render(request, "core/forgot_password.html")

def confirm_email(request, email):
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        return redirect('core:login')

    return render(request, "core/confirm_email.html", {'email': email})