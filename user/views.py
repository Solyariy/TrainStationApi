from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import (
    JWTAuthentication,
)

from user.serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)

    def get_object(self):
        return self.request.user
