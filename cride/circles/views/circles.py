"""Circles views."""

# Django REST Framework
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Serializer
from cride.circles.serializers import CircleModelSerializer

# Model
from cride.circles.models import Circle, Membership


class CircleViewSet(viewsets.ModelViewSet):
    """Circle view set."""

    serializer_class = CircleModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Restric list to public-only"""
        queryset = Circle.objects.all()

        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset
    
    def perform_create(self,serializer):
        """Assign a circle admin."""

        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10
        )