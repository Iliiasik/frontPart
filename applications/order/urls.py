from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderActivationAPIView, UserOrderHistoryAPIView
from . import views

router = DefaultRouter()
router.register('', OrderViewSet)

urlpatterns = [
    path('activate/<str:activation_code>/', OrderActivationAPIView.as_view(), name='order-activation'),
    path('qr-code/<int:pk>/', views.OrderQRCodeAPIView.as_view(), name='order-qr-code'),
    path('user-order-history/', UserOrderHistoryAPIView.as_view(), name='user-order-history'),
]

urlpatterns += router.urls
