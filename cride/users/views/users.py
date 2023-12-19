"""Users views"""

# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Serializer
from cride.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer
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
