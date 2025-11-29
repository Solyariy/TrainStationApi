from rest_framework.serializers import ValidationError

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
                raise ValidationError(
                    "Seat number can't be greater than places_in_cargo; "
                    f"maximum = {train.places_in_cargo}"
                )
            if ticket.get("cargo") > train.cargo_num:
                raise ValidationError(
                    "Cargo with such number does not exist; "
                    f"maximum = {train.cargo_num}"
                )

    def validate_same_places(self):
        unique_places = set(
            (d["seat"], d["cargo"], d["journey"].id)
            for d in self.data.get("tickets")
        )
        if len(unique_places) != len(
            self.data.get("tickets")
        ):
            raise ValidationError(
                "There are tickets with the same seats"
            )

    def validate(self):
        self.validate_places()
        self.validate_same_places()


class JourneyValidator:
    def __init__(self, attrs: dict):
        self.data = attrs

    def validate_time(self):
        if self.data.get("departure_time") >= self.data.get(
            "arrival_time"
        ):
            raise ValidationError(
                "You can't arrive before departure"
            )

    def validate(self):
        self.validate_time()
