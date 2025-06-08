from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .models import PointOfSale
from .serializers import PointOfSaleSerializer


class SyncInventory(APIView):
    def post(self, request):
        data = request.data
        # здесь логика обновления остатков
        return Response({"status": "ok"})


class PointOfSaleViewSet(viewsets.ModelViewSet):
    queryset = PointOfSale.objects.all()
    serializer_class = PointOfSaleSerializer
