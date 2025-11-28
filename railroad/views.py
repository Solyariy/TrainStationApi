from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from railroad.models import (
    Crew,
    Journey,
    Order,
    Route,
    Station,
    Train,
    TrainType,
)
from railroad.serializers import (
    CrewSerializer,
    JourneyListSerializer,
    JourneySerializer,
    OrderSerializer,
    RouteDetailSerializer,
    RouteListSerializer,
    RouteSerializer,
    StationSerializer,
    TrainDetailSerializer,
    TrainListSerializer,
    TrainSerializer,
    TrainTypeSerializer,
)


class JourneyViewSet(ModelViewSet):
    queryset = Journey.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer
        return JourneySerializer


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class CrewViewSet(ModelViewSet):
    serializer_class = CrewSerializer
    queryset = Crew.objects.all()


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
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer
