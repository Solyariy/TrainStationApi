from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)
from railroad.filters import JourneyFilter, TrainFilter
from railroad.models import (
    Crew,
    Journey,
    Order,
    Route,
    Station,
    Ticket,
    Train,
    TrainType,
)
from railroad.serializers import (
    CrewDetailSerializer,
    CrewSerializer,
    JourneyDetailSerializer,
    JourneyListSerializer,
    JourneySerializer,
    OrderSerializer,
    RouteDetailSerializer,
    RouteListSerializer,
    RouteSerializer,
    StationSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
    TrainDetailSerializer,
    TrainListSerializer,
    TrainSerializer,
    TrainTypeSerializer,
)


class TicketViewSet(ReadOnlyModelViewSet):
    queryset = Ticket.objects.select_related(
        "journey__route__source",
        "journey__route__destination",
        "journey__train__train_type",
        "order__user",
    )

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        return TicketDetailSerializer


class JourneyViewSet(ModelViewSet):
    filterset_class = JourneyFilter
    queryset = Journey.objects.select_related(
        "route__source",
        "route__destination",
        "train__train_type",
    )

    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer
        if self.action == "retrieve":
            return JourneyDetailSerializer
        return JourneySerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.select_related(
        "user"
    ).prefetch_related("tickets")
    serializer_class = OrderSerializer


class CrewViewSet(ModelViewSet):
    queryset = Crew.objects

    def get_queryset(self):
        if self.action == "retrieve":
            return self.queryset.select_related(
                "journey__route__source",
                "journey__route__destination",
                "journey__train__train_type",
            )
        return self.queryset.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CrewDetailSerializer
        return CrewSerializer


class TrainTypeViewSet(ModelViewSet):
    serializer_class = TrainTypeSerializer
    queryset = TrainType.objects.all()


class TrainViewSet(ModelViewSet):
    filterset_class = TrainFilter
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
