from django_filters import rest_framework as filters

from railroad.models import Journey, Train


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
            "arrival_time",
            "departure_time",
            "route__destination",
            "route__source",
            "train__train_type",
        )


class TrainFilter(filters.FilterSet):
    types = filters.CharFilter(
        field_name="train_type__name",
        lookup_expr="icontains",
    )

    class Meta:
        model = Train
        fields = ("train_type",)
