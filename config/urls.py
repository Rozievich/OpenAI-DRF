from django.contrib import admin
from django.urls import path
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="OpenAI ChatBot API",
      default_version='v1.0',
      description="OpenAI asistant api integration",
      terms_of_service="https://github.com/Rozievich/OpenAI-DRF",
      contact=openapi.Contact(email="oybekrozievich@gmail.com"),
      license=openapi.License(name="Rozievich"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),

]