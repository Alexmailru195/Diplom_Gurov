from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from orders.models import Order


class SalesReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except (TypeError, ValueError):
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        completed_orders = Order.objects.filter(
            status='completed',
            created_at__range=[start_date, end_date]
        )

        total_sales = sum(order.total_price() for order in completed_orders)
        total_orders = completed_orders.count()

        return Response({
            'start_date': start_date_str,
            'end_date': end_date_str,
            'total_orders': total_orders,
            'total_sales': total_sales,
        })
