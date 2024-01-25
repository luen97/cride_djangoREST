"""Circles views."""

# Django REST Framework
from rest_framework import viewsets, mixins

# Permissions 
from cride.circles.permissions import IsCircleAdmin
from rest_framework.permissions import IsAuthenticated

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Serializer
from cride.circles.serializers import CircleModelSerializer

# Model
from cride.circles.models import Circle, Membership




class CircleViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """Circle view set."""

    serializer_class = CircleModelSerializer
    lookup_field = 'slug_name'

    # Filters
    # This filters are made in the get_queryset
    filter_backends = (SearchFilter,OrderingFilter,DjangoFilterBackend)
    search_fields = ('slug_name','name')
    ordering_field = ('rides_offered','rides_taken','name','created','member_limit')
    ordering = ('-members__count','rides_offered','-rides_taken')
    filter_fields = ('verified','is_limited') # Possible by DjFilterBackend



    def get_queryset(self):
        """Restric list to public-only"""
        queryset = Circle.objects.all()

        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset
    
    def get_permissions(self):
        """Assing permissions based on actions."""
        permissions = [IsAuthenticated]

        if self.action in ['update','partial_update']:
            permissions.append(IsCircleAdmin)

        return [permission() for permission in permissions]
    
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