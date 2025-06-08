from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog_list, name='catalog-list'),
    path('<int:product_id>/', views.product_detail, name='product-detail'),
]