from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import TemplateView

schema_view = get_schema_view(
   openapi.Info(
      title="Assignment API",
      default_version='v1',
      description="Backend Developer Intern - API",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(("api.urls","api"), namespace="v1")),
    
    # Swagger + ReDoc
    path("swagger(<format>\.json|\.yaml)", schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path("docs/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('', TemplateView.as_view(template_name='frontend/index.html')),
]
