from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

from utils.constants import ACCEPTED_FILE_EXTENSIONS

extension_validator = FileExtensionValidator(ACCEPTED_FILE_EXTENSIONS)


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
    created_by = models.ForeignKey(User, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    media_file = models.FileField(
        upload_to="uploads/", default=None, validators=[extension_validator]
    )
    price = models.FloatField()
    thumbnail_url = models.URLField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:  # type: ignore
        ordering = ("name",)

    def __str__(self):
        return self.name
