from django.contrib import admin
from .models import Item, ItemAmount, Check, CheckItem

admin.site.register(Item)
admin.site.register(ItemAmount)
admin.site.register(Check)
admin.site.register(CheckItem)
