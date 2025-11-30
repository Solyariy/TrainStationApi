from django.db.models import Q
from rest_framework.serializers import ValidationError

from railroad.models import Station


class OrderValidatorMixin:
    @staticmethod
    def validate_places(attrs, errors):
        for ticket in attrs.get("tickets"):
            journey = ticket.get("journey")
            train = journey.train
            if ticket.get("seat") <= 0:
                errors.append(
                    "Seat can't be negative value"
                )
            if ticket.get("cargo") <= 0:
                errors.append(
                    "Cargo can't be negative value"
                )
            if ticket.get("seat") > train.places_in_cargo:
                errors.append(
                    "Seat number can't be greater than places_in_cargo; "
                    f"maximum = {train.places_in_cargo}"
                )
            if ticket.get("cargo") > train.cargo_num:
                errors.append(
                    "Cargo with such number does not exist; "
                    f"maximum = {train.cargo_num}"
                )

    @staticmethod
    def validate_same_places(attrs, errors):
        unique_places = set(
            (d["seat"], d["cargo"], d["journey"].id)
            for d in attrs.get("tickets")
        )
        if len(unique_places) != len(attrs.get("tickets")):
            errors.append(
                "There are tickets with the same seats"
            )

    def validate(self, attrs):
        errors = []
        self.validate_places(attrs, errors)
        self.validate_same_places(attrs, errors)
        if errors:
            raise ValidationError(errors)
        return attrs


class JourneyValidatorMixin:
    @staticmethod
    def validate_time(attrs, errors):
        if attrs.get("departure_time") >= attrs.get(
            "arrival_time"
        ):
            errors.append(
                "You can't arrive before departure"
            )

    @staticmethod
    def validate_train_schedule(attrs, errors):
        train = attrs.get("train")
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
            errors.append(
                "Train will be preoccupied on these dates"
            )

    def validate(self, attrs):
        errors = []
        self.validate_time(attrs, errors)
        self.validate_train_schedule(attrs, errors)
        if errors:
            raise ValidationError(errors)
        return attrs


class RouteValidatorMixin:
    @staticmethod
    def validate_stations(attrs, errors):
        if (
            attrs.get("source").id
            == attrs.get("destination").id
        ):
            errors.append(
                "Source can't be equal to destination"
            )

    @staticmethod
    def validate_distance_non_negative(attrs, errors):
        if attrs.get("distance") <= 0:
            errors.append(
                "Distance should be non negative value"
            )

    def validate(self, attrs):
        errors = []
        self.validate_stations(attrs, errors)
        self.validate_distance_non_negative(attrs, errors)
        if errors:
            raise ValidationError(errors)
        return attrs


class StationValidatorMixin:
    @staticmethod
    def validate_unique_coordinates(attrs, errors):
        if Station.objects.filter(
            latitude=attrs.get("latitude"),
            longitude=attrs.get("longitude"),
        ).exists():
            errors.append(
                "Station with such coordinates already exists"
            )

    def validate(self, attrs):
        errors = []
        self.validate_unique_coordinates(attrs, errors)
        if errors:
            raise ValidationError(errors)
        return attrs


class TrainValidatorMixin:
    @staticmethod
    def validate_non_negativity(attrs, errors):
        if attrs.get("cargo_num") < 0:
            errors.append(
                "The number of cargo must be non negative value"
            )
        if attrs.get("places_in_cargo") < 0:
            errors.append(
                "The number of places in cargo must be non negative value"
            )
        if (
            attrs.get("cargo_num") == 0
            and attrs.get("places_in_cargo") != 0
        ):
            errors.append(
                "Train without cargo can't have non zero places"
            )

    def validate(self, attrs):
        errors = []
        self.validate_non_negativity(attrs, errors)
        if errors:
            raise ValidationError(errors)
        return attrs
