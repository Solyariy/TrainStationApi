from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from railroad.models import (
    Route,
    Station,
    Train,
    TrainType,
)
from railroad.serializers import (
    RouteListSerializer,
    RouteSerializer,
    StationSerializer,
    TrainListSerializer,
    TrainSerializer,
    TrainTypeSerializer, TrainDetailSerializer,
)


class TrainTypeViewSet(ModelViewSet):
    serializer_class = TrainTypeSerializer
    queryset = TrainType.objects.all()


class TrainViewSet(ModelViewSet):
    queryset = Train.objects.select_related("train_type")

    def get_serializer_class(self):
        if self.action == "list":
            return TrainListSerializer
        if self.action == "retrieve":
            return TrainDetailSerializer
        return TrainSerializer


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
