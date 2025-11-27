from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from railroad.models import (
    Route,
    Station,
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
        source="train_type",
        read_only=True
    )

    class Meta:
        model = Train
        fields = "__all__"
        extra_kwargs = {
            "train_type": {"write_only": True}
        }

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
