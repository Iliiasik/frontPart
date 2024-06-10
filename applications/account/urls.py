from django.urls import path
from . import views
from applications.account.views import *
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='apartmen/login.html'), name='login'),
    # path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('register_view/', views.register_view, name='register_view'),
    path('register_done/', views.register_done, name='register_done'),
    # path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('user-info/', UserInfoAPIView.as_view(), name='user-info'),
    # path('activate/<uuid:activation_code>/', ActivationAPIView.as_view()),
    path('activate/<str:activation_code>/', views.ActivationAPIView.as_view(), name='activate'),
    path('change_password/', ChangePasswordAPIView.as_view()),
    path('forgot_password/', ForgotPasswordAPIView.as_view()),
    path('forgot_password_confirm/', ForgotPasswordConfirmAPIView.as_view()),
    path('owner-apartment/', views.OwnerUserApartmentAPIView.as_view(), name='owner_apartment'),
    path('owner_apartment_info/<str:email>/', OwnerApartmentInfoByEmailView.as_view(), name='owner_apartment_info_by_email'),
    path('test_celery/', send_mail_view)
]
