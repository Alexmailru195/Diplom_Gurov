from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from .models import Category, Product


# ===== Тесты моделей =====
class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Офисная техника")
        self.product = Product.objects.create(
            name="Ламинатор A4",
            description="Ламинатор для документов формата A4",
            price=3500,
            category=self.category
        )

    def test_category_creation(self):
        """Проверяет создание категории 'Офисная техника'"""
        self.assertEqual(self.category.name, "Офисная техника")

    def test_product_creation(self):
        """Проверяет создание продукта 'Ламинатор A4'"""
        self.assertEqual(self.product.name, "Ламинатор A4")
        self.assertEqual(self.product.price, 3500)
        self.assertEqual(self.product.category.name, "Офисная техника")


# ===== Тесты API =====
class ProductApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Офисная техника")
        self.product_data = {
            "name": "Шредер для бумаг",
            "description": "Устройство для уничтожения конфиденциальных документов",
            "price": 4500,
            "slug": "shreder-dlya-bumag",
            "category_id": self.category.id  # ← Добавь эту строку
        }
        self.url = reverse('product-list')

    def test_create_product(self):
        """Проверка создания продукта через API"""
        response = self.client.post(self.url, self.product_data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, "Шредер для бумаг")

    def test_get_products(self):
        """Проверка получения списка продуктов через API"""
        Product.objects.create(
            name="Ламинатор A4",
            description="Ламинатор для документов формата A4",
            price=3500,
            category=self.category
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
