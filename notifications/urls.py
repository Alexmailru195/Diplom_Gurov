from django.urls import path
from .views import NotificationListAPIView


urlpatterns = [
    path('api/notifications/', NotificationListAPIView.as_view(), name='notification-list'),
]
