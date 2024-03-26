import asyncio

from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .file_handler import delete_file, upload_file
from .forms import FeedbackForm, ItemForm
from .models import Category, Item, ItemFeedback, ItemReport
from .thumbnail_generator import generate_thumbnail


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

    feedbacks = ItemFeedback.objects.filter(item=item)
    average_rating = feedbacks.aggregate(avg_rating=Avg("rating"))["avg_rating"]
    average_rating = int(average_rating) if average_rating is not None else 0

    return render(
        request,
        "items/item.html",
        {
            "item": item,
            "related_items": related_items,
            "feedbacks": feedbacks,
            "average_rating": average_rating,
        },
    )


@login_required
def add(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            media_file = request.FILES["media_file"]
            item.media_blob_name = asyncio.run(upload_file(media_file))
            item.thumbnail_url = generate_thumbnail(media_file)
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
            if request.FILES["media_file"]:
                media_file = request.FILES["media_file"]
                asyncio.run(delete_file(form.instance.media_blob_name))
                blob_name = asyncio.run(upload_file(media_file))
                form.instance.media_blob_name = blob_name
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
    asyncio.run(delete_file(item.media_blob_name))
    item.delete()
    return redirect("dashboard:index")


@login_required
def feedback_form(request, id):
    item = get_object_or_404(Item, id=id)
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_text = form.cleaned_data["feedback"]
            rating = form.cleaned_data["rating"]
            ItemFeedback.objects.create(
                user=request.user, item=item, feedback=feedback_text, rating=rating
            )
            return redirect(reverse("items:thank_you"))
    else:
        form = FeedbackForm()
    return render(request, "items/feedback_form.html", {"form": form, "item": item})


@login_required
def thank_you_view(request):
    return render(request, "items/thank_you.html")


@login_required
def report_item(request, id):
    item = get_object_or_404(Item, id=id)
    report, created = ItemReport.objects.get_or_create(
        item=item, reported_by=request.user
    )

    return render(
        request, "items/report_item.html", {"item_reported": created, "item": item}
    )
