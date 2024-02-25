from django import forms
from utils.constants import HTML_ACCEPTED_FILE_EXTENSIONS

from .models import Item

INPUT_CLASSES = "w-full py-4 px-2 rounded-md border"


class ItemForm(forms.ModelForm):
    class Meta:  # type: ignore
        model = Item
        fields = (
            "category",
            "name",
            "description",
            "media_file",
            "price",
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
                attrs={"class": "mb-2", "accept": HTML_ACCEPTED_FILE_EXTENSIONS}
            ),
            "price": forms.NumberInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Price"}
            ),
        }
