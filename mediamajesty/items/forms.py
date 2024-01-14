from django import forms

from .models import Item

INPUT_CLASSES = "w-full py-4 px-2 rounded-sm border"


class AddNewItemForm(forms.ModelForm):
    class Meta:  # type: ignore
        model = Item
        fields = (
            "category",
            "name",
            "description",
            "media_file",
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
            "media_file": forms.FileInput(attrs={"class": "mb-4"}),
            "price": forms.NumberInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Price"}
            ),
            "thumbnail_url": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Thumbnail URL"}
            ),
        }


class EditItemForm(forms.ModelForm):
    class Meta:  # type: ignore
        model = Item
        fields = (
            "name",
            "description",
            "media_file",
            "price",
            "thumbnail_url",
            "is_sold",
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
            "media_file": forms.FileInput(attrs={"class": "mb-4"}),
            "price": forms.NumberInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Price"}
            ),
            "thumbnail_url": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Thumbnail URL"}
            ),
        }