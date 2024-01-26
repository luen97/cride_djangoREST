"""Rides serializer."""

# Django REST Framework
from rest_framework import serializer

# Models
from cride.rides.models import Ride

# Utilities
from datetime import timedelta
from django.utils import timezone

class CreateRideSerializer(serializer.ModelSerializer):
    """Create ride serializer."""

    # CurrentUserDefault return the user given in the context
    offered_by = serializer.HiddenField(default=serializer.CurrentUserDefault())
    avaliable_seats = serializer.IntegerField(min_value=1,max_value=15)

    class Meta:
        """Meta class."""

        model = Ride
        # exclude the circle, it's already given in the serializer context
        # that is loaded in the viewset
        exclude = ('offered_in','passangers','rating','is_active')

    def validate_departure_date(self,data):
        """Verify date is not in the past"""

        min_date = timezone.now() + timedelta(minutes=10)
        
        if data < min_date:
            raise serializer.ValidationError(
                'Departure time must be at least pass the next 20 minutes window.'
            )
        return data
    