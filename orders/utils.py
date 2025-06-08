from datetime import datetime
from .models import Order


def get_sales_report(start_date=None, end_date=None):
    orders = Order.objects.filter(status='completed')
    if start_date:
        orders = orders.filter(created_at__gte=start_date)
    if end_date:
        orders = orders.filter(created_at__lte=end_date)
    total_sales = sum(order.cart.total_price() for order in orders)
    return {'total_orders': orders.count(), 'total_sales': total_sales}
