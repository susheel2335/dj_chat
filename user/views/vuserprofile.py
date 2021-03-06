"""
Edicion de usuarios (perfil)
"""

# third-party
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Django
from django.contrib.auth import authenticate

# local Django
from user.serializers import (
    UserHeavySerializer,
    UserSerializer,
    PasswordResetSerializer
)


class UserProfileView(APIView):
    """
    ...
    """
    permission_classes = (IsAuthenticated,)
    serializer = UserSerializer
    response_serializer = UserHeavySerializer

    def post(self, request, format=None):
        """
        ...
        """
        response = self.serializer(request.user, data=request.data)
        if response.is_valid():
            result = response.save()
            res = UserHeavySerializer(result)
            return Response(res.data, status=status.HTTP_200_OK)

        return Response(response.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    """
    ...
    """
    permission_classes = (IsAuthenticated,)
    serializer = PasswordResetSerializer

    def post(self, request, format=None):
        """
        ...
        """
        response = self.serializer(data=request.data)
        if response.is_valid():
            user = authenticate(
                username=request.user.username,
                password=response.validated_data['old_password'],
            )

            if user is None:
                return Response(
                    'old password incorrect',
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(response.validated_data['new_password'])
            user.save()
            return Response(status=status.HTTP_200_OK)

        return Response(
            response.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
