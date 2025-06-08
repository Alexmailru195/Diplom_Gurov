from django.db import models
from products.models import Product
from pos.models import PointOfSale


class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'


class Inventory(models.Model):
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Склад'
    )
    point_of_sale = models.ForeignKey(
        PointOfSale,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Точка продаж'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    last_updated = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')

    class Meta:
        unique_together = ('warehouse', 'point_of_sale', 'product')
        verbose_name = 'Остаток товара'
        verbose_name_plural = 'Остатки товаров'

    def __str__(self):
        location = self.warehouse or self.point_of_sale or "Неизвестное место"
        return f"{location}: {self.product} — {self.quantity} шт."
