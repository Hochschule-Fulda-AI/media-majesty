from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ItemForm, FeedbackForm
from .models import Category, Item, UserFeedback
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Item, ItemReport


def index(request):
    search = request.GET.get("search", "")
    category_id = request.GET.get("category", 0)
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False, is_approved=True)

    if min_price and max_price:
        items = items.filter(price__range=(min_price, max_price))

    if min_price:
        items = items.filter(price__gte=min_price)

    if max_price:
        items = items.filter(price__lte=max_price)

    if category_id != 0:
        items = items.filter(category_id=category_id)

    if search != "":
        items = items.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )

    return render(
        request,
        "items/index.html",
        {
            "items": items,
            "search": search,
            "categories": categories,
            "category_id": int(category_id),
        },
    )


def item(request, id):
    item = get_object_or_404(Item, id=id)
    related_items = Item.objects.filter(
        category=item.category, is_sold=False, is_approved=True
    ).exclude(id=id)
    return render(
        request, "items/item.html", {"item": item, "related_items": related_items}
    )


@login_required
def add(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect("items:item", id=item.id)
    else:
        form = ItemForm()

    return render(
        request,
        "items/form.html",
        {
            "form": form,
            "title": "Add new Item",
        },
    )


@login_required
def edit(request, id):
    item = get_object_or_404(Item, id=id, created_by=request.user)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.instance.is_approved = False
            form.save()
            return redirect("items:item", id=id)
    else:
        form = ItemForm(instance=item)

    return render(
        request,
        "items/form.html",
        {
            "form": form,
            "title": "Edit Item",
        },
    )


@login_required
def delete(request, id):
    item = get_object_or_404(Item, id=id, created_by=request.user)
    item.delete()
    return redirect("dashboard:index")


def feedback_form(request, id):
    item = get_object_or_404(Item, id=id)

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data["feedback"]
            rating = form.cleaned_data["rating"]
            UserFeedback.objects.create(
                user=request.user, item=item, feedback=feedback, rating=rating
            )
            return redirect("items:thank_you")
    else:
        form = FeedbackForm()

    return render(request, "items/feedback_form.html", {"form": form, "item": item})


def thank_you_view(request):
    return render(request, "items/thank_you.html")


@login_required
def report_item(request, id):
    item = get_object_or_404(Item, id=id)
    report, created = ItemReport.objects.get_or_create(item=item, reported_by=request.user)

    # Check if the item has been reported and pass the information to the template
    return render(request, 'items/report_item.html', {'item_reported': created, 'item': item})