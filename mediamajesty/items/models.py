from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:  # type: ignore
        ordering = ("name",)
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.ForeignKey(
        Category, related_name="items", on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        User, related_name="owned_items", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.FloatField()
    media_blob_name = models.CharField(max_length=255)
    thumbnail_url = models.URLField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:  # type: ignore
        ordering = ("name",)

    def __str__(self):
        return self.name


class ItemFeedback(models.Model):
    user = models.ForeignKey(User, related_name="feedbacks", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="feedbacks", on_delete=models.CASCADE)
    rating = models.IntegerField()
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.item} rating ({self.user}): {self.rating}"
