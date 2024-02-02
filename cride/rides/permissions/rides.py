"""Rides permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission

class IsRideOwner(BasePermission):
    """Verify requesting user is the ride owner."""

    def has_object_permission(self,request,view,obj):
        """Verify requesting user is the ride owner."""
        return request.user == obj.offered_by
    
class IsNotRideOwner(BasePermission):
    """Verify requesting user is the ride owner."""

    def has_object_permission(self,request,view,obj):
        """Verify requesting user is the ride owner."""
        return not request.user == obj.offered_by
