from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AddNewItemForm, EditItemForm
from .models import Item


def index(request, id):
    item = get_object_or_404(Item, id=id)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(
        id=id
    )
    return render(
        request, "items/index.html", {"item": item, "related_items": related_items}
    )


@login_required
def add_new_item(request):
    if request.method == "POST":
        form = AddNewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect("items:index", id=item.id)
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
def edit_item(request, id):
    item = get_object_or_404(Item, id=id, created_by=request.user)

    if request.method == "POST":
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()
            return redirect("items:index", id=id)
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
def delete_item(request, id):
    item = get_object_or_404(Item, id=id, created_by=request.user)
    item.delete()
    return redirect("dashboard:index")