from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from collects.views import CollectViewSet, PaymentViewSet


router = DefaultRouter()
router.register(r"collects", CollectViewSet, basename="collect")
router.register(r"payments", PaymentViewSet, basename="payment")


urlpatterns = [
    path("admin/", admin.site.urls),

    # API
    path("api/", include(router.urls)),

    # Swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]