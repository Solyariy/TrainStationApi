from django_filters import rest_framework as filters

from railroad.models import Crew, Journey, Order, Route, Station, Ticket, Train


class JourneyFilter(filters.FilterSet):
    departure_after = filters.DateFilter(
        field_name="departure_time",
        lookup_expr="gt",
    )
    departure_before = filters.DateFilter(field_name="departure_time", lookup_expr="lt")
    arrival_after = filters.DateFilter(
        field_name="arrival_time",
        lookup_expr="gt",
    )
    arrival_before = filters.DateFilter(field_name="arrival_time", lookup_expr="lt")
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


class StationFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    latitude_range = filters.NumericRangeFilter(
        field_name="latitude",
    )
    longitude_range = filters.NumericRangeFilter(
        field_name="longitude",
    )

    class Meta:
        model = Station
        fields = ("name", "latitude_range", "longitude_range")


class TicketFilter(filters.FilterSet):
    class Meta:
        model = Ticket
        fields = ("journey", "cargo")


class OrderFilter(filters.FilterSet):
    created_after = filters.DateTimeFilter(
        field_name="created_at", lookup_expr="date__gte"
    )
    created_before = filters.DateTimeFilter(
        field_name="created_at", lookup_expr="date__lte"
    )

    class Meta:
        model = Order
        fields = ("created_after", "created_before", "user")


class RouteFilter(filters.FilterSet):
    source = filters.CharFilter(field_name="source__name", lookup_expr="icontains")
    destination = filters.CharFilter(
        field_name="destination__name", lookup_expr="icontains"
    )
    distance_gt = filters.NumberFilter(field_name="distance", lookup_expr="gte")
    distance_lt = filters.NumberFilter(field_name="distance", lookup_expr="lte")

    class Meta:
        model = Route
        fields = ("source", "destination", "distance_gt", "distance_lt")
