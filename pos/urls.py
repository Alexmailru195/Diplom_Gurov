from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PointOfSaleViewSet


router = DefaultRouter()
router.register(r'points', PointOfSaleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]