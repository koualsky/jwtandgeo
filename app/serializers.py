from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Geolocalization

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )

        return user

    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "password",
        )


class GeolocalizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocalization
        fields = "__all__"
