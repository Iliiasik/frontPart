from rest_framework.routers import DefaultRouter
from . import views

# Создаем объект DefaultRouter для автоматической генерации URL-маршрутов
router = DefaultRouter()

# Регистрируем ваши представления с помощью роутера
router.register(r'questions', views.QuestionsViewSet)
router.register(r'complaints', views.ComplaintViewSet)
router.register(r'sendproblems', views.SendProblemViewSet)

urlpatterns = []

urlpatterns += router.urls
