from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import AddNewItemForm, EditItemForm
from .models import Category, Item
from faker import Faker
from django.contrib.auth.models import User  # Add this import at the beginning of the file
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views import View



def items(request):
    search = request.GET.get("search", "")
    category_id = request.GET.get("category", 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if search:
        items = items.filter(Q(name__icontains=search) | Q(description__icontains=search))

    return render(
        request,
        "items/items.html",
        {
            "items": items,
            "search": search,
            "categories": categories,
            "category_id": int(category_id),
        },
    )

class SearchSuggestionsView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("query", "")
        suggestions = Item.objects.filter(name__icontains=query).values('id', 'name')
        suggestions_list = [{'id': suggestion['id'], 'name': suggestion['name']} for suggestion in suggestions]
        return JsonResponse(suggestions_list, safe=False)
    
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


def generate_dummy_posts(request):
    fake = Faker()

    category_names = ["Electronics", "Clothing", "Books", "Furniture", "Toys"]
    categories = [Category.objects.create(name=name) for name in category_names]

    for _ in range(100):  
        category = fake.random_element(elements=categories)
        user = User.objects.first() 

        item = Item.objects.create(
            category=category,
            created_by=user,
            name=fake.text(50),
            description=fake.text(),
            media_url="https://picsum.photos/500/300",
            price=fake.random_number(2),
            is_sold=False,
        )

    return render(request, 'items/index.html', {'message': 'Dummy posts added successfully'})