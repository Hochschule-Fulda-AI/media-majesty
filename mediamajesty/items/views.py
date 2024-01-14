from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .forms import AddNewItemForm, EditItemForm
from .models import Category, Item


def index(request):
    search = request.GET.get("search", "")
    category_id = request.GET.get("category", 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False, is_approved=True)

    if category_id:
        items = items.filter(category_id=category_id)

    if search:
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
        form = AddNewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect("items:item", id=item.id)
    else:
        form = AddNewItemForm()

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
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.instance.is_approved = False
            form.save()
            return redirect("items:item", id=id)
    else:
        form = EditItemForm(instance=item)

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
