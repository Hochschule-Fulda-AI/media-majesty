from django.shortcuts import render, get_object_or_404
from .models import Item


def index(request, id):
    item = get_object_or_404(Item, pk=id)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(
        pk=id
    )
    return render(
        request, "items/index.html", {"item": item, "related_items": related_items}
    )
