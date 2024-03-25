import magic
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from utils.constants import (
    ACCEPTED_FILE_EXTENSIONS,
    ACCEPTED_FILE_MIME_TYPES,
    HTML_ACCEPTED_FILE_EXTENSIONS,
)

from .models import Item


def mime_validator(file):
    mime = magic.Magic(mime=True)
    file_mime_type = mime.from_buffer(file.read(1024))
    if file_mime_type not in ACCEPTED_FILE_MIME_TYPES:
        raise ValidationError(
            f"File type {file_mime_type} is not supported. "
            f"Supported file types are {ACCEPTED_FILE_EXTENSIONS}"
        )


extension_validator = FileExtensionValidator(ACCEPTED_FILE_EXTENSIONS)

INPUT_CLASSES = "w-full py-4 px-2 rounded-md border"


class ItemForm(forms.ModelForm):
    media_file = forms.FileField(validators=[extension_validator, mime_validator])

    class Meta:  # type: ignore
        model = Item
        fields = (
            "category",
            "name",
            "description",
            "price",
            "thumbnail_url",
        )
        widgets = {
            "category": forms.Select(attrs={"class": INPUT_CLASSES}),
            "name": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Item name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": INPUT_CLASSES,
                    "rows": 2,
                    "placeholder": "Item description",
                }
            ),
            "media_file": forms.FileInput(
                attrs={"class": "mb-2", "accept": HTML_ACCEPTED_FILE_EXTENSIONS},
            ),
            "price": forms.NumberInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Price"}
            ),
            "thumbnail_url": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Thumbnail URL"},
            ),
        }


class FeedbackForm(forms.Form):
    feedback = forms.CharField(
        label="Leave a feedback regarding your purchase", widget=forms.Textarea
    )
    rating = forms.IntegerField(label="Rating", min_value=1, max_value=5)
