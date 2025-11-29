from django.db import transaction
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

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


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = "__all__"


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = "__all__"


class TrainDetailSerializer(serializers.ModelSerializer):
    train_type_info = TrainTypeSerializer(
        source="train_type", read_only=True
    )
    total_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Train
        exclude = ("train_type",)


class TrainListSerializer(serializers.ModelSerializer):
    train_type = serializers.CharField(
        source="train_type.name"
    )
    total_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Train
        fields = "__all__"


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"

    def validate(self, attrs):
        if attrs.get("source") == attrs.get("destination"):
            raise ValidationError(
                "Source and Destination cannot be the same station.",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return super().validate(attrs)


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


class JourneySerializer(serializers.ModelSerializer):
    total_time_hr = serializers.FloatField(read_only=True)

    class Meta:
        model = Journey
        fields = "__all__"

    def validate(self, attrs):
        data = super(
            serializers.ModelSerializer, self
        ).validate(attrs)
        val = validators.JourneyValidator(attrs)
        val.validate()
        return data


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
            "journey",
        )
        extra_kwargs = {"full_name": {"read_only": True}}


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        exclude = ("order",)


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    # user = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )
    class Meta:
        model = Order
        fields = "__all__"
        extra_kwargs = {"created_at": {"read_only": True}}

    def validate(self, attrs):
        data = super(
            serializers.ModelSerializer, self
        ).validate(attrs)
        val = validators.OrderValidator(attrs)
        val.validate()
        return data

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
