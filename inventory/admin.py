from django.contrib import admin
from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'point_of_sale', 'quantity', 'last_updated')
    list_filter = ('point_of_sale', 'product')
    search_fields = ('product__name',)
    readonly_fields = ('last_updated',)
