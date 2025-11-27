from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from railroad.models import (
    Route,
    Station,
)


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
