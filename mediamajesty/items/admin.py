from django.contrib import admin

from .models import Category, Item, ItemFeedback, ItemReport

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(ItemFeedback)
admin.site.register(ItemReport)
