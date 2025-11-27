from django.urls import include, path
from rest_framework.routers import DefaultRouter

from railroad.views import (
    RouteViewSet,
    StationViewSet,
    TrainTypeViewSet,
    TrainViewSet, CrewViewSet, OrderViewSet, JourneyViewSet,
)

router = DefaultRouter()
router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)
router.register("trains/types", TrainTypeViewSet)
router.register("trains", TrainViewSet)
router.register("crew", CrewViewSet)
router.register("orders", OrderViewSet)
router.register("journeys", JourneyViewSet)

app_name = "railroad"

urlpatterns = [path("", include(router.urls))]
