from django.http import JsonResponse
from django.contrib.auth.models import User
from faker import Faker

from items.models import Category, Item

fake = Faker()


def users(_):
    created_users = []
    for _ in range(10):
        username = fake.name().lower().replace(" ", "_")
        email = username + "@hochschule-fulda.de"
        password = fake.password()
        _, created = User.objects.get_or_create(
            username=username, defaults={"email": email, "password": password}
        )
        created_users.append(
            {
                "username": username,
                "email": email,
                "created": created,
            }
        )
    return JsonResponse({"users": created_users})


def items(_):
    created_items = []
    for _ in range(10):
        user = fake.random_element(User.objects.all())
        category = fake.random_element(Category.objects.all())
        name = fake.sentence(nb_words=3)
        description = fake.text()
        price = fake.pyint(min_value=5, max_value=50)
        thumbnail = fake.image_url(width=1920, height=1080)
        _, created = Item.objects.get_or_create(
            name=name,
            defaults={
                "created_by": user,
                "category": category,
                "description": description,
                "price": price,
                "thumbnail_url": thumbnail,
            },
        )
        created_items.append(
            {
                "created_by": user.username,
                "category": category.name,
                "name": name,
                "description": description,
                "price": price,
                "thumbnail_url": thumbnail,
                "created": created,
            }
        )
    return JsonResponse({"items": created_items})


def categories(_):
    category_names = [
        "Photographs",
        "Videos",
        "Music",
        "Digital Illustrations",
        "EBooks",
        "Websites",
    ]
    created_categories = []
    for name in category_names:
        _, created = Category.objects.get_or_create(name=name)
        created_categories.append({"name": name, "created": created})

    return JsonResponse({"categories": created_categories})