"""Users views"""

# Django REST Framework
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import (
    AllowAny, 
    IsAuthenticated
)
from cride.users.permissions import IsAccountOwner

# Serializer
from cride.circles.serializers import CircleModelSerializer
from cride.users.serializers.profiles import ProfileModelSerializer
from cride.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer
    )

# Models
from cride.users.models import User
from cride.circles.models import Circle

class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """User view set.
    
    Handle signup, login and account verification.
    """

    queryset = User.objects.filter(is_active=True,is_client=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        """Assign permission based on action."""
        if self.action in ['signup','login','verify']:
            permissions = [AllowAny]
        elif self.action in ['retrieve','update','partial_update','profile']:
            permissions = [IsAuthenticated,IsAccountOwner]
        else:
            permissions = [IsAuthenticated]

        return [permission() for permission in permissions]

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User signup """
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Only validated users got a token
        user = serializer.save()
        data = UserModelSerializer(user).data
         
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'acces_token': token
        }

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification"""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message':'Congratulations, now go share some rides!'
        }
         
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put','patch'])
    def profile(self, request,*args,**kwargs):
        """Update profile data."""
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # The user we are using here below is the
        # one of the session with it's data updated
        # in the serializer.save() line above
        data = UserModelSerializer(user).data
        return Response(data)

    def retrieve(self,request,*args,**kwargs):
        """Add extra data to the response."""
        response = super().retrieve(request,*args,**kwargs)
        circles = Circle.objects.filter(
            members=request.user,
            membership__is_active=True
        )
        data = {
            'user': response.data,
            'circles': CircleModelSerializer(circles,many=True).data
        }
        response.data = data
        return response
