from rest_framework.routers import DefaultRouter
from applications.spam.views import ContactAPIView

router = DefaultRouter()
router.register('', ContactAPIView)

urlpatterns = []
urlpatterns.extend(router.urls)

