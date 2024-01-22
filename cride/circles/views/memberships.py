"""Circles memberships views"""

# Django REST Framework
from rest_framework import mixins,viewsets
from rest_framework.generics import get_object_or_404

# Models 
from cride.circles.models import Circle, Membership

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember

# Serializers
from cride.circles.serializers import MembershipModelSerializer

class MembershipViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Circle membership viewset"""

    serializer_class = MembershipModelSerializer

    """Given that the circle slug_name comes in the url, 
    we must take it from there to the query 
    We want the circle instance be available in 
    all the validations of th eview, for that we 
    added to the class"""
    def dispatch(self,request,*args,**kwargs):
        """Verify that the circle exits"""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle,slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request,*args,**kwargs)
    
    def get_permissions(self):
        """Assing permissions based on actions"""
        permissions = [IsAuthenticated,IsActiveCircleMember]
        return [p() for p in permissions]
    
    def get_queryset(self):
        """Return circle members"""
        return Membership.objects.filter(
            circle=self.circle,
            is_active=True  
        )
    
    def get_object(self):
        """Return the circle member by using the user's username"""
        return get_object_or_404(
            Membership,
            user__username=self.kwargs['pk'],
            circle=self.circle,
            is_active=True
        )
    
    def perform_destroy(self, instance):
        """Disable membership"""
        instance.is_active=False
        instance.save()
    


