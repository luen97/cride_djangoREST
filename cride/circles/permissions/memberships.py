"""Membership permissios classes"""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Model
from cride.circles.models import Membership 

class IsActiveCircleMember(BasePermission):
    """Allow acces only to circle members
    
    Expect that views implementing this permission
    have a circle attribute assigned"""

    def has_permission(self,request,view):
        """Verify user is active member of the circle"""
        try:
            Membership.objects.get(
                user=request.user,
                circle=view.circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True
    
class IsSelfMember(BasePermission):
    """Allow access only to member owner."""

    def has_permission(self, request, view):
        """Let object permission grant access"""

        obj = view.get_object()
        # import ipdb; ipdb.set_trace()

        return self.has_object_permission(request, view, obj)
    
    def has_object_permission(self, request, view, obj):
        """Allow access only if member is owned by the requesting user."""
        return request.user == obj.user
