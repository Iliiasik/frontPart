from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from applications.giftcard.views import GiftCardAPIView

router = DefaultRouter()

router.register(r'', GiftCardAPIView)

urlpatterns = []

urlpatterns += router.urls

