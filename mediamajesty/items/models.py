import magic
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from utils.constants import ACCEPTED_FILE_EXTENSIONS, ACCEPTED_FILE_MIME_TYPES

extension_validator = FileExtensionValidator(ACCEPTED_FILE_EXTENSIONS)


def validate_file_mime_type(file):
    mime = magic.Magic(mime=True)
    file_mime_type = mime.from_buffer(file.read(1024))
    if file_mime_type not in ACCEPTED_FILE_MIME_TYPES:
        raise ValidationError(
            f"File type {file_mime_type} is not supported. "
            f"Supported file types are {ACCEPTED_FILE_EXTENSIONS}"
        )


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
        upload_to="uploads/",
        default=None,
        validators=[extension_validator, validate_file_mime_type],
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


class UserFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    feedback = models.TextField()

    def __str__(self):
        return f"Feedback for {self.item.name} by {self.user.username}"
    

class ItemReport(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item.name} reported by {self.reported_by.username}"
