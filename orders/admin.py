from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'delivery_type', 'payment_method', 'created_at')
    list_filter = ('status', 'delivery_type', 'payment_method')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('user', 'cart', 'status')
        }),
        ('Доставка и оплата', {
            'fields': ('delivery_type', 'payment_method')
        }),
        ('Информация', {
            'fields': ('created_at',)
        }),
    )
