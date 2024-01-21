import os
import uuid
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from faker import Faker

from items.models import Category, Item
from utils.constants import CATEGORIES, SEED_NUM
from utils.functions import download_image_from_url

fake = Faker()


@user_passes_test(lambda u: u.is_staff)  # type: ignore
def categories(_):
    created_categories = []
    for name in CATEGORIES:
        _, created = Category.objects.get_or_create(name=name)
        created_categories.append({"name": name, "created": created})

    return JsonResponse({"categories": created_categories})


@user_passes_test(lambda u: u.is_staff)  # type: ignore
def users(_):
    created_users = []
    for _ in range(SEED_NUM):
        username = fake.name().lower().replace(" ", "_")
        email = username + "@informatik.hs-fulda.de"
        password = fake.password()
        user, created = User.objects.get_or_create(
            username=username, defaults={"email": email}
        )
        user.set_password(password)
        user.save()
        created_users.append(
            {
                "username": username,
                "email": email,
                "created": created,
            }
        )
    return JsonResponse({"users": created_users})


@user_passes_test(lambda u: u.is_staff)  # type: ignore
def items(_):
    created_items = []
    for _ in range(SEED_NUM):
        category = fake.random_element(Category.objects.all())
        user = fake.random_element(User.objects.all().exclude(is_staff=True))
        name = fake.sentence(nb_words=3)
        description = fake.text()
        price = fake.pyint(min_value=0, max_value=50)
        thumbnail = f"https://picsum.photos/seed/{name}/1920/1080"
        media_file = download_image_from_url(thumbnail)
        item, created = Item.objects.get_or_create(
            name=name,
            defaults={
                "created_by": user,
                "category": category,
                "description": description,
                "price": price,
                "thumbnail_url": thumbnail,
            },
        )
        with open(media_file.name, "rb") as file:  # type: ignore
            item.media_file.save(
                uuid.uuid4().hex + "." + file.name.split(".")[-1],  # type: ignore
                file,
                save=True,
            )
        media_file.close()  # type: ignore
        os.remove(media_file.name)  # type: ignore
        created_items.append(
            {
                # "created_by": user.username,
                "category": category.name,
                "name": name,
                "description": description,
                "price": price,
                "thumbnail_url": thumbnail,
                "created": created,
            }
        )
    return JsonResponse({"items": created_items})
