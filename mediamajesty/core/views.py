from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect

from items.models import Category, Item
from .forms import SignUpForm


def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
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

def inbox(request):
    return render(request, "core/inbox.html")
