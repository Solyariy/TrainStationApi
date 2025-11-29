from django_filters import rest_framework as filters

from railroad.models import Journey, Train, Crew


class JourneyFilter(filters.FilterSet):
    departure_after = filters.DateFilter(
        field_name="departure_time",
        lookup_expr="gt",
    )
    departure_before = filters.DateFilter(
        field_name="departure_time", lookup_expr="lt"
    )
    arrival_after = filters.DateFilter(
        field_name="arrival_time",
        lookup_expr="gt",
    )
    arrival_before = filters.DateFilter(
        field_name="arrival_time", lookup_expr="lt"
    )
    destination = filters.CharFilter(
        field_name="route__destination__name",
        lookup_expr="icontains",
    )
    source = filters.CharFilter(
        field_name="route__source__name",
        lookup_expr="icontains",
    )
    train_type = filters.CharFilter(
        field_name="train__train_type__name",
        lookup_expr="icontains",
    )

    class Meta:
        model = Journey
        fields = (
            "departure_after",
            "departure_before",
            "arrival_after",
            "arrival_before",
            "destination",
            "source",
            "train_type",
        )


class TrainFilter(filters.FilterSet):
    type = filters.CharFilter(
        field_name="train_type__name",
        lookup_expr="icontains",
    )

    class Meta:
        model = Train
        fields = ("type",)


class CrewFilter(filters.FilterSet):
    first_name = filters.CharFilter(
        field_name="first_name",
        lookup_expr="icontains",
    )
    last_name = filters.CharFilter(
        field_name="last_name",
        lookup_expr="icontains",
    )

    class Meta:
        model = Crew
        fields = ("first_name", "last_name", "journey")
