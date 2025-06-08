from rest_framework import serializers
from .models import Product, Category, ProductAttribute, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['key', 'value']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        required=True,
        label='Категория'
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'slug',
            'created_at',
            'category',
            'category_id',
            'attributes',
            'images',
        ]
        read_only_fields = ['id', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Проверяем, есть ли 'request' в контексте
        request = self.context.get('request')

        # Если это запрос на изменение или создание — скрываем read-only поля
        if request and request.method in ['POST', 'PUT', 'PATCH']:
            self.fields.pop('category', None)
            self.fields.pop('attributes', None)
            self.fields.pop('images', None)
