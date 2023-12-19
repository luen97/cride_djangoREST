"""Users views"""

# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Serializer
from cride.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer
    )

class UserLoginAPIView(APIView):
    """Users login view"""

    def post(self, request, *args,**kwargs):
        """Handle HTTP POST request."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'acces_token': token
        }

        return Response(data, status=status.HTTP_201_CREATED)

class UserSignUpAPIView(APIView):
    """Users sigup view"""

    def post(self, request, *args,**kwargs):
        """Handle HTTP POST request."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Only validated users got a token
        user = serializer.save()
        data = UserModelSerializer(user).data
         
        return Response(data, status=status.HTTP_201_CREATED)