from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Category, ProductImage, ProductAttribute


# === INLINE для изображений товара ===
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_tag',)
    fields = ('image', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-width: 200px; max-height: 200px;">'
        return "-"

    image_tag.short_description = "Изображение"
    image_tag.allow_tags = True


# === INLINE для характеристик товара ===
class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1
    fields = ('key', 'value')


# === Админка: Товар ===
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'created_at')
    search_fields = ('name', 'description', 'category__name')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)
    inlines = [ProductImageInline, ProductAttributeInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'price', 'category')
        }),
        ('Дополнительно', {
            'fields': ('created_at',)
        }),
    )


# === Админка: Категория ===
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('indented_name',)
    search_fields = ('name',)
    list_filter = ('parent',)
    autocomplete_fields = ['parent']

    # Отображение дерева категорий с отступами
    def indented_name(self, instance):
        depth = getattr(instance, 'get_level', lambda: 0)()
        return format_html('&nbsp;&nbsp;' * depth + '{}', instance.name)

    indented_name.short_description = 'Категория'


# === Админка: Изображения ===
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_tag')
    search_fields = ('product__name',)
    list_filter = ('product',)
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-width: 200px; max-height: 200px;">'
        return "-"

    image_tag.short_description = "Изображение"
    image_tag.allow_tags = True


# === Админка: Характеристики товаров ===
@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'key', 'value')
    search_fields = ('product__name', 'key', 'value')
    list_filter = ('key',)
