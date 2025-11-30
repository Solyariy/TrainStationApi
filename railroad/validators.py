from django.db.models import Q
from rest_framework.serializers import ValidationError

# available tickets
# train is free at the time of journey
# crew is free at the journey dates


class OrderValidatorMixin:
    @staticmethod
    def validate_places(attrs):
        for ticket in attrs.get("tickets"):
            journey = ticket.get("journey")
            train = journey.train
            if ticket.get("seat") <= 0:
                raise ValidationError(
                    "Seat can't be negative value"
                )
            if ticket.get("cargo") <= 0:
                raise ValidationError(
                    "Cargo can't be negative value"
                )
            if ticket.get("seat") > train.places_in_cargo:
                raise ValidationError(
                    "Seat number can't be greater than places_in_cargo; "
                    f"maximum = {train.places_in_cargo}"
                )
            if ticket.get("cargo") > train.cargo_num:
                raise ValidationError(
                    "Cargo with such number does not exist; "
                    f"maximum = {train.cargo_num}"
                )

    @staticmethod
    def validate_same_places(attrs):
        unique_places = set(
            (d["seat"], d["cargo"], d["journey"].id)
            for d in attrs.get("tickets")
        )
        if len(unique_places) != len(attrs.get("tickets")):
            raise ValidationError(
                "There are tickets with the same seats"
            )

    def validate(self, attrs):
        self.validate_places(attrs)
        self.validate_same_places(attrs)
        return attrs


class JourneyValidatorMixin:
    @staticmethod
    def validate_time(attrs):
        if attrs.get("departure_time") >= attrs.get(
            "arrival_time"
        ):
            raise ValidationError(
                "You can't arrive before departure"
            )

    @staticmethod
    def validate_train_schedule(attrs):
        train = attrs.get("train")
        if not train.journeys.exists():
            return
        conditions = [
            Q(
                arrival_time__gte=attrs.get(
                    "departure_time"
                )
            ),
            Q(
                departure_time__lte=attrs.get(
                    "arrival_time"
                )
            ),
        ]
        if train.journeys.filter(
            conditions[0] & conditions[1]
        ).exists():
            raise ValidationError(
                "Train will be preoccupied on these dates"
            )

    def validate(self, attrs):
        self.validate_time(attrs)
        self.validate_train_schedule(attrs)
        return attrs


class RouteValidatorMixin:
    @staticmethod
    def validate_stations(attrs):
        if (
            attrs.get("source").id
            == attrs.get("destination").id
        ):
            raise ValidationError(
                "Source can't be equal to destination"
            )
