from django.db import models
from cart.models import Cart
from users.models import User


ORDER_STATUS_CHOICES = (
    ('created', 'Создан'),
    ('paid', 'Оплачен'),
    ('processing', 'В обработке'),
    ('shipped', 'Отправлен'),
    ('completed', 'Завершен'),
    ('cancelled', 'Отменён')
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    delivery_type = models.CharField(max_length=50)  # курьер / самовывоз
    payment_method = models.CharField(max_length=50)  # онлайн / наличными
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user}"

    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())
