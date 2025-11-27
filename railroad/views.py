from rest_framework.viewsets import ModelViewSet

from railroad.models import (
    Route,
    Station,
)
from railroad.serializers import (
    RouteListSerializer,
    RouteSerializer,
    StationSerializer,
)


class StationViewSet(ModelViewSet):
    serializer_class = StationSerializer
    queryset = Station.objects.all()


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.select_related(
        "source", "destination"
    )

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        return RouteSerializer
