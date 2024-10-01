from rest_framework import serializers

class FlightOfferSerializer(serializers.Serializer):
    origin = serializers.CharField(required=True)
    destination = serializers.CharField(required=True)
    departureDate = serializers.DateField(required=True)  # Validate date format
    adults = serializers.IntegerField(required=False, default=1)  # Optional with default value
    max = serializers.IntegerField(required=False, default=1)  # Optional with default value
    nocache = serializers.BooleanField(required=False, default=False)  # Add nocache as a boolean

