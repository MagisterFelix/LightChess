from django.contrib.auth import logout
from django.middleware.csrf import rotate_token
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.server.serializers import AuthorizationSerializer, RegistrationSerializer
from core.server.utils import AuthorizationUtils


class AuthorizationView(APIView):

    serializer_class = AuthorizationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        rotate_token(request)

        response = Response(status=status.HTTP_200_OK)
        AuthorizationUtils.set_auth_cookies(response, serializer.validated_data)

        return response


class DeauthorizationView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.COOKIES.get("sessionid") and logout(request)

        response = Response(status=status.HTTP_204_NO_CONTENT)
        AuthorizationUtils.remove_auth_cookies(response)

        return response


class RegistrationView(APIView):

    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)
