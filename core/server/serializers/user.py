from rest_framework.serializers import ModelSerializer

from core.server.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "image",)
