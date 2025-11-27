from django.urls import include, path
from rest_framework.routers import DefaultRouter

from railroad.views import (
    RouteViewSet,
    StationViewSet,
    TrainTypeViewSet,
    TrainViewSet,
)

router = DefaultRouter()
router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)
router.register("trains/types", TrainTypeViewSet)
router.register("trains", TrainViewSet)

app_name = "railroad"

urlpatterns = [path("", include(router.urls))]
