from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
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
    TrainTypeSerializer, CrewImageSerializer, CrewListSerializer, TrainImageSerializer, StationImageSerializer,
    StationListDetailSerializer,
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
        if self.action == "list":
            return CrewListSerializer
        if self.action == "upload_image":
            return CrewImageSerializer
        return CrewSerializer

    @action(
        methods=["POST"],
        url_path="upload-image",
        detail=True
    )
    def upload_image(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        if self.action == "upload_image":
            return TrainImageSerializer
        return TrainSerializer

    @action(
        methods=["POST"],
        url_path="upload-image",
        detail=True
    )
    def upload_image(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class StationViewSet(ModelViewSet):
    queryset = Station.objects.all()

    def get_serializer_class(self):
        if self.action == "upload_image":
            return StationImageSerializer
        if self.action in ("list", "retrieve"):
            return StationListDetailSerializer
        return StationSerializer

    @action(
        methods=["POST"],
        url_path="upload-image",
        detail=True
    )
    def upload_image(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


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
