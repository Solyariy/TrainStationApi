from django.db import models
from django.db.models import F, Q
from rest_framework import status


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
                violation_error_message="Such Station already exists"
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
