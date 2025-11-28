from rest_framework import serializers

# available tickets
# train is free at the time of journey
# crew is free at the journey dates


class OrderValidator:
    def __init__(self, attrs: dict):
        self.data = attrs

    def validate_places(self):
        for ticket in self.data.get("tickets"):
            journey = ticket.get("journey")
            train = journey.train
            if ticket.get("seat") > train.places_in_cargo:
                raise serializers.ValidationError(
                    "Seat number can't be greater than places_in_cargo; "
                    f"maximum = {train.places_in_cargo}"
                )
            if ticket.get("cargo") > train.cargo_num:
                raise serializers.ValidationError(
                    "Cargo with such number does not exist; "
                    f"maximum = {train.cargo_num}"
                )

    def validate_same_places(self):
        unique_places = set(self.data.get("tickets"))
        if len(unique_places) != len(
            self.data.get("tickets")
        ):
            raise serializers.ValidationError(
                "There are tickets with the same seats"
            )

    def validate(self):
        self.validate_places()
        self.validate_same_places()
