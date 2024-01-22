from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Item


@user_passes_test(lambda u: u.is_staff)  # type: ignore
def pending_items(request):
    items = Item.objects.filter(is_approved=False)
    return render(request, "items/pending_items.html", {"items": items})


@user_passes_test(lambda u: u.is_staff)  # type: ignore
def pending_item(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, "items/pending_item.html", {"item": item})


@user_passes_test(lambda u: u.is_staff)  # type: ignore
def approve_item(request, id):
    item = get_object_or_404(Item, id=id)
    item.is_approved = True
    item.save()
    return redirect("items:pending_items")

@user_passes_test(lambda u: u.is_staff)
def report_item(request, id):
    item = get_object_or_404(Item, id=id)
    
    # Check if the item is already reported
    if item.is_reported:
        messages.warning(request, f'The item "{item.name}" is already reported.')
    else:
        item.is_approved = False
        item.is_reported = True
        item.save()
        messages.success(request, f'The item "{item.name}" has been reported and disapproved.')

    return redirect("items:pending_items")
