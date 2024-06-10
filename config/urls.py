"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="Samirkk",
      default_version='v1',
      description="Contacs is we",
      contact=openapi.Contact(email="samirkk@gmail.com"),
   ),
   public=True,
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('applications.apartment.urls')),
    path('apartment/', include('applications.apartment.urls')),  # Приложение apartment
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/account/', include('applications.account.urls')),
    path('api/v1/apartment/', include('applications.apartment.urls')),
    path('api/v1/order/', include('applications.order.urls')),
    path('api/v1/spam/', include('applications.spam.urls')),
    path('api/v1/help-center/', include('applications.helpcenter.urls')),
    path('api/v1/giftcard/', include('applications.giftcard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

