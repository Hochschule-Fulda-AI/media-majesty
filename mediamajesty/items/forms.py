from django import forms

from .models import Item

INPUT_CLASSES = "w-full py-4 px-2 rounded-sm border"


class AddNewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ("category", "name", "description", "media_url", "price", "thumbnail")
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
            "media_url": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Media URL"}
            ),
            "price": forms.NumberInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Price"}
            ),
            "thumbnail": forms.FileInput(attrs={"class": INPUT_CLASSES}),
        }


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ("name", "description", "media_url", "price", "thumbnail", "is_sold")
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
            "media_url": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Media URL"}
            ),
            "price": forms.NumberInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Price"}
            ),
            "thumbnail": forms.FileInput(attrs={"class": INPUT_CLASSES}),
        }
