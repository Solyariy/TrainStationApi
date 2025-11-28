from django_filters import rest_framework as filters

from railroad.models import Journey


class JourneyFilter(filters.FilterSet):
    class Meta:
        model = Journey
        fields = ("departure_time", "arrival_time")

