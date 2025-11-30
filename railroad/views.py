from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, extend_schema_view
from railroad.filters import JourneyFilter, TrainFilter, CrewFilter, StationFilter, TicketFilter, OrderFilter, \
    RouteFilter
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
    CrewImageSerializer,
    CrewListSerializer,
    CrewSerializer,
    JourneyDetailSerializer,
    JourneyListSerializer,
    JourneySerializer,
    OrderSerializer,
    RouteDetailSerializer,
    RouteListSerializer,
    RouteSerializer,
    StationImageSerializer,
    StationListDetailSerializer,
    StationSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
    TrainDetailSerializer,
    TrainImageSerializer,
    TrainListSerializer,
    TrainSerializer,
    TrainTypeSerializer,
)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="journey",
                type=OpenApiTypes.INT,
                description="Filter tickets by journey_id"
            ),
            OpenApiParameter(
                name="cargo",
                type=OpenApiTypes.INT,
                description="Returns tickets from specific cargo (better use with journey filter)"
            )
        ]
    )
)
class TicketViewSet(ReadOnlyModelViewSet):
    filterset_class = TicketFilter
    queryset = Ticket.objects.select_related(
        "journey__route__source",
        "journey__route__destination",
        "journey__train__train_type",
        "order__user",
    )

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.queryset.filter(
                order__user=self.request.user
            )
        return self.queryset

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        return TicketDetailSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="departure_after",
                type=OpenApiTypes.DATETIME,
                description="Returns journeys with departure after specified time"
            ),
            OpenApiParameter(
                name="departure_before",
                type=OpenApiTypes.DATETIME,
                description="Returns journeys with departure before specified time"
            ),
            OpenApiParameter(
                name="arrival_after",
                type=OpenApiTypes.DATETIME,
                description="Returns journeys with arrival after specified time"
            ),
            OpenApiParameter(
                name="arrival_before",
                type=OpenApiTypes.DATETIME,
                description="Returns journeys with arrival before specified time"
            ),
            OpenApiParameter(
                name="destination",
                type=OpenApiTypes.STR,
                description="Filter journeys by destination"
            ),
            OpenApiParameter(
                name="source",
                type=OpenApiTypes.STR,
                description="Filter journeys by source"
            ),
            OpenApiParameter(
                name="train_type",
                type=OpenApiTypes.STR,
                description="Filter journeys by train type"
            )
        ],
    )
)
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


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="created_after",
                type=OpenApiTypes.DATETIME,
                description="Returns orders created after specified date"
            ),
            OpenApiParameter(
                name="created_before",
                type=OpenApiTypes.DATETIME,
                description="Returns orders created before specified date"
            ),
            OpenApiParameter(
                name="user",
                type=OpenApiTypes.INT,
                description="Returns orders of specific user"
            ),
        ]
    )
)
class OrderViewSet(ModelViewSet):
    filterset_class = OrderFilter
    queryset = Order.objects
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(
            user_id=self.request.user.id
        ).select_related(
            "user"
        ).prefetch_related("tickets")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="first_name",
                type=OpenApiTypes.STR,
                description="Filter crew by first name"
            ),
            OpenApiParameter(
                name="last_name",
                type=OpenApiTypes.STR,
                description="Filter crew by last name"
            ),
            OpenApiParameter(
                name="journey",
                type=OpenApiTypes.INT,
                description="Returns crew of specific journey"
            ),
        ]
    )
)
class CrewViewSet(ModelViewSet):
    filterset_class = CrewFilter
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
        detail=True,
    )
    def upload_image(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )


class TrainTypeViewSet(ModelViewSet):
    serializer_class = TrainTypeSerializer
    queryset = TrainType.objects.all()


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="type",
                type=OpenApiTypes.STR,
                description="Filter trains by their types"
            )
        ],
    )
)
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
        detail=True,
    )
    def upload_image(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                description="Filter stations by name"
            ),
            OpenApiParameter(
                name="latitude_range",
                type=OpenApiTypes.INT,
                description="Returns station within specified latitude range"
            ),
            OpenApiParameter(
                name="longitude_range",
                type=OpenApiTypes.INT,
                description="Returns station within specified longitude range"
            )
        ]
    )
)
class StationViewSet(ModelViewSet):
    filterset_class = StationFilter
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
        detail=True,
    )
    def upload_image(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="source",
                type=OpenApiTypes.STR,
                description="Filter stations by source name"
            ),
            OpenApiParameter(
                name="destination",
                type=OpenApiTypes.STR,
                description="Filter stations by destination name"
            ),
            OpenApiParameter(
                name="distance_gt",
                type=OpenApiTypes.INT,
                description="Returns router with distance greater than specified"
            ),
            OpenApiParameter(
                name="distance_lt",
                type=OpenApiTypes.INT,
                description="Returns router with distance less than specified"
            )
        ]
    )
)
class RouteViewSet(ModelViewSet):
    filterset_class = RouteFilter
    queryset = Route.objects.select_related(
        "source", "destination"
    )

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer
