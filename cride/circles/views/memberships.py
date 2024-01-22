"""Circles memberships views"""

# Django REST Framework
from rest_framework import mixins,viewsets
from rest_framework.generics import get_object_or_404

# Models 
from cride.circles.models import Circle, Membership

# Serializers
from cride.circles.serializers import MembershipModelSerializer

class MembershipViewSet(mixins.ListModelMixin,
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
    
    def get_queryset(self):
        """Return circle members"""
        return Membership.objects.filter(
            circle=self.circle,
            is_active=True  
        )
    


