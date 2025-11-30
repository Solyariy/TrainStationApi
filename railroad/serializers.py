from django.db import transaction
from rest_framework import serializers

from railroad import validators
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
from railroad.validators import TrainValidatorMixin


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = "__all__"


class TrainSerializer(
    TrainValidatorMixin, serializers.ModelSerializer
):
    class Meta:
        model = Train
        exclude = ("train_type",)


class TrainDetailSerializer(serializers.ModelSerializer):
    train_type_info = TrainTypeSerializer(
        source="train_type", read_only=True
    )
    total_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Train
        fields = "__all__"


class TrainListSerializer(serializers.ModelSerializer):
    train_type = serializers.CharField(
        source="train_type.name", allow_null=True
    )
    total_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Train
        fields = "__all__"


class TrainImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ("id", "image")


class StationSerializer(
    validators.StationValidatorMixin,
    serializers.ModelSerializer,
):
    class Meta:
        model = Station
        exclude = ("image",)


class StationListDetailSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = Station
        fields = "__all__"


class StationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "image")


class RouteSerializer(
    validators.RouteValidatorMixin,
    serializers.ModelSerializer,
):
    distance = serializers.IntegerField()

    class Meta:
        model = Route
        fields = "__all__"


class RouteDetailSerializer(serializers.ModelSerializer):
    source = StationSerializer(read_only=True)
    destination = StationSerializer(read_only=True)

    class Meta:
        model = Route
        fields = "__all__"


class RouteListSerializer(serializers.ModelSerializer):
    source_station = serializers.CharField(
        source="source.name"
    )
    destination_station = serializers.CharField(
        source="destination.name"
    )

    class Meta:
        model = Route
        exclude = ("source", "destination")


class JourneySerializer(
    validators.JourneyValidatorMixin,
    serializers.ModelSerializer,
):
    total_time_hr = serializers.FloatField(read_only=True)

    class Meta:
        model = Journey
        fields = "__all__"


class JourneyListSerializer(JourneySerializer):
    route = serializers.CharField(read_only=True)
    train = serializers.CharField(read_only=True)
    taken_seats = serializers.IntegerField(read_only=True)
    free_seats = serializers.IntegerField(read_only=True)


class JourneyDetailSerializer(JourneySerializer):
    route = RouteDetailSerializer(read_only=True)
    train = TrainDetailSerializer(read_only=True)


class CrewSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Crew
        exclude = ("image",)


class CrewListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Crew
        fields = "__all__"


class CrewDetailSerializer(serializers.ModelSerializer):
    journey = JourneyDetailSerializer(read_only=True)

    class Meta:
        model = Crew
        fields = (
            "id",
            "first_name",
            "last_name",
            "full_name",
            "image",
            "journey",
        )
        extra_kwargs = {"full_name": {"read_only": True}}


class CrewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "image")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        exclude = ("order",)


class OrderSerializer(
    validators.OrderValidatorMixin,
    serializers.ModelSerializer,
):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"
        extra_kwargs = {
            "created_at": {"read_only": True},
            "user": {
                "read_only": True,
                "default": serializers.CurrentUserDefault(),
            },
        }

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")

        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            tickets_to_create = [
                Ticket(order=order, **item)
                for item in tickets_data
            ]
            Ticket.objects.bulk_create(tickets_to_create)

        return order


class TicketListSerializer(serializers.ModelSerializer):
    journey = JourneyListSerializer(read_only=True)
    order = serializers.CharField(read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"


class TicketDetailSerializer(serializers.ModelSerializer):
    journey = JourneyDetailSerializer(read_only=True)
    order = serializers.CharField(read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"
