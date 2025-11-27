from django.urls import include, path
from rest_framework.routers import DefaultRouter

from railroad.views import (
    RouteViewSet,
    StationViewSet,
)

router = DefaultRouter()
router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)

app_name = "railroad"

urlpatterns = [path("", include(router.urls))]
