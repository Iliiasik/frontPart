from django.urls import path, include
from . import views
from applications.apartment.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('category', CategoryModelViewSet)
router.register('comments', CommentModelViewSet)
router.register('image', ImageModelViewSet)
router.register('', ApartmentAPIVIew, basename='apartment')

urlpatterns = [
path('apartment/<int:pk>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('', main_page, name='main_page'),
    path('get/<str:name>/', UserActionHistoryAPIView.as_view(), name='user-action-history'),
    path('recommendations/', views.ApartmentAPIVIew.as_view({'get': 'get_recommendations'}),
         name='apartment-recommendations'),
    path('<int:pk>/', views.apartment_detail, name='apartment_detail'),
    path('apartment/<int:pk>/', views.apartment_detail, name='apartment_detail')
]

urlpatterns += router.urls
