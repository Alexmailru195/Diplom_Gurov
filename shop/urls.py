from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# === Локальные ViewSet'ы из приложений ===
from products.views import ProductViewSet, CategoryViewSet
from orders.views import OrderViewSet
from pos.views import PointOfSaleViewSet
from users.views import UserViewSet
from cart.views import CartViewSet

# === Настройка Swagger / OpenAPI документации ===
schema_view = get_schema_view(
    openapi.Info(
        title="Интернет-магазин API",
        default_version='v1',
        description="API интернет-магазина для дипломного проекта",
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# === Инициализация роутера и регистрация ViewSet'ов ===
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'points', PointOfSaleViewSet, basename='point-of-sale')
router.register(r'users', UserViewSet, basename='user')
router.register(r'cart', CartViewSet, basename='cart')

# === Основные URL проекта ===
urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Документация через Swagger UI и ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Все API маршруты через router подключаются под префиксом /api/
    path('api/', include(router.urls)),

    # Маршруты для модулей (например, отчёты или кастомные API)
    path('api/reports/', include('reports.urls')),

    # Обычные маршруты сайта (HTML-страницы)
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('catalog/', include('catalog.urls')),
    path('cart/', TemplateView.as_view(template_name='cart/cart.html'), name='cart'),
    path('profile/', include('user_profile.urls')),
    path('orders/', include('orders.urls')),
    path('accounts/', include('accounts.urls')),
]
