import math

from rest_framework import serializers


class EstimateRequestSerializer(serializers.Serializer):
    """Validates type and range. Ranges come from docs/02-srs.md."""

    sqft = serializers.FloatField(min_value=300, max_value=10_000)
    bedrooms = serializers.IntegerField(min_value=1, max_value=10)
    age = serializers.FloatField(min_value=0, max_value=100)
    location_rating = serializers.IntegerField(min_value=1, max_value=5)

    def _finite(self, value):
        # NaN slips past min/max checks (NaN comparisons are always False).
        if not math.isfinite(value):
            raise serializers.ValidationError("A valid number is required.")
        return value

    def validate_sqft(self, value):
        return self._finite(value)

    def validate_age(self, value):
        return self._finite(value)
