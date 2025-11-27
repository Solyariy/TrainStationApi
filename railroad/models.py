from django.db import models
from django.db.models import F, Q
from rest_framework import status

from app import settings


class Journey(models.Model):
    route = models.ForeignKey("Route", on_delete=models.SET_NULL, null=True)
    train = models.ForeignKey("Train", on_delete=models.SET_NULL, null=True)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.route} | {self.departure_time} -> {self.arrival_time}"



# class Ticket(models.Model):
#     cargo = models.IntegerField()
#     seat = models.IntegerField()
#     journey = models.ForeignKey("Journey")


class Order(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    def __str__(self):
        return self.user.get_full_name() + " " + self.created_at


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class TrainType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=255)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(
        TrainType,
        on_delete=models.SET_NULL,
        related_name="trains",
        null=True,
    )

    def __str__(self):
        return f"{self.train_type} | {self.name}"


class Station(models.Model):
    name = models.CharField(max_length=255, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("latitude", "longitude"),
                name="unique_all_stations",
                violation_error_code=status.HTTP_400_BAD_REQUEST,
                violation_error_message="Such Station already exists",
            ),
        ]

    def __str__(self):
        return self.name.title()


class Route(models.Model):
    source = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="sourced_routes",
    )
    destination = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="destined_routes",
    )
    distance = models.IntegerField(null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="source_not_equal_destination_constraint",
                condition=~Q(
                    source__exact=F("destination")
                ),
            )
        ]

    def __str__(self):
        return f"{self.source} -> {self.destination}"
