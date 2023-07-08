from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.server.models import User


class AuthorizationSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        attr = attrs["username"]

        user = User.objects.get_or_none(username=attr)

        if user is None or not user.check_password(attrs.get("password")):
            raise AuthenticationFailed("No user was found with these credentials.")

        if not user.is_active:
            raise AuthenticationFailed("User is blocked.")

        return super().validate(attrs)


class RegistrationSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "password",)
        extra_kwargs = {
            "password": {
                "write_only": True
            },
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
