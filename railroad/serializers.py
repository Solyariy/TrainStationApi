from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from railroad.models import (
    Crew,
    Journey,
    Order,
    Route,
    Station,
    Train,
    TrainType,
)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        extra_kwargs = {"created_at": {"read_only": True}}


class CrewSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Crew
        fields = "__all__"


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

    class Meta:
        model = Train
        exclude = ("train_type",)


class TrainListSerializer(serializers.ModelSerializer):
    train_type = serializers.CharField(
        source="train_type.name"
    )

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
    class Meta:
        model = Journey
        fields = "__all__"


class JourneyListSerializer(serializers.ModelSerializer):
    route = serializers.CharField()
    train = serializers.CharField()

    class Meta:
        model = Journey
        fields = "__all__"
