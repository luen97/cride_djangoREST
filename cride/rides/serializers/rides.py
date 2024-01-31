"""Rides serializer."""

# Django REST Framework
from rest_framework import serializers

# Models
from cride.rides.models import Ride
from cride.circles.models import Membership

# Utilities
from datetime import timedelta
from django.utils import timezone

class RideModelSerializer(serializers.ModelSerializer):
    """Ride model serializer."""

    class Meta:
            """Meta class."""

            model = Ride
            fields = '__all__'
            read_only_fields = (
                'offered_by',
                'offered_in',
                'rating'
            )
   

class CreateRideSerializer(serializers.ModelSerializer):
    """Create ride serializer."""

    # CurrentUserDefault return the user given in the context
    offered_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    available_seats = serializers.IntegerField(min_value=1,max_value=15)

    class Meta:
        """Meta class."""

        model = Ride
        # exclude the circle, it's already given in the serializer context
        # that is loaded in the viewset
        exclude = ('offered_in','passengers','rating','is_active')

    def validate_departure_date(self,data):
        """Verify date is not in the past"""

        min_date = timezone.now() + timedelta(minutes=10)
        
        if data < min_date:
            raise serializers.ValidationError(
                'Departure time must be at least pass the next 20 minutes window.'
            )
        return data
    
    def validate(self,data):
        """Validate.
        
        Verify that the person who offers the ride is member
        and also the same user making the request.
        """
        if self.context['request'].user != data['offered_by']:
            return serializers.ValidationError('Rides offered on behalf of others are not allowed.')
        
        user = data['offered_by']
        circle = self.context['circle']
        try:
            membership = Membership.objects.get(
                user=user,
                circle=circle
            )
        except Membership.DoesNotExist:
            return serializers.ValidationError('User is not an active member of the circle.')
        
        if data['arrival_date'] <= data['departure_date']:
            return serializers.ValidationError('Departure date must happen before arrival date.')
        
        self.context['membership'] = membership
        return data
    
    def create(self,data):
        """Create ride and update stats."""
        circle = self.context['circle']
        ride = Ride.objects.create(**data,offered_in=circle)

        # Circle
        circle.rides_offered += 1
        circle.save()

        # Membership
        membership = self.context['membership']
        membership.rides_offered += 1
        circle.save()

        # Profile
        profile = data['offered_by'].profile
        profile.rides_offered += 1
        profile.save()

        return ride
