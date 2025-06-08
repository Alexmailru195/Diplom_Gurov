from django.contrib import admin
from .models import PointOfSale


@admin.register(PointOfSale)
class PointOfSaleAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'lat', 'lon', 'working_hours')
    search_fields = ('name', 'address')
    list_filter = ('working_hours',)
