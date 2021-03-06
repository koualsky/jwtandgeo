import json
import re
import socket

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Geolocalization
from .serializers import GeolocalizationSerializer, UserSerializer


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {"message": "Hello, World!"}
        return Response(content)


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class GeolocalizationView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        # Get parameter and do the validation
        address = request.POST.get("address")
        try:
            re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", address)
            address = socket.gethostbyname(address)
        except Exception as e:
            return Response(
                {
                    "message": f"{e}. Please provide a valid IP address in body parameters."
                }
            )

        # Get or Create
        r = requests.get(
            f"http://api.ipstack.com/{address}?access_key={settings.GEOLOCALIZATION_KEY}&format=1"
        )
        content = json.loads(r.text)
        ip_exists = Geolocalization.objects.filter(ip=content.get("ip"))
        if ip_exists:
            return Response(
                {
                    "message": f"Geolocalization with this ip ({address}) already exists in the database."
                }
            )
        else:
            try:
                Geolocalization.objects.create(
                    ip=content.get("ip"),
                    type=content.get("type"),
                    continent_code=content.get("continent_code"),
                    continent_name=content.get("continent_name"),
                    country_code=content.get("country_code"),
                    country_name=content.get("country_name"),
                    region_code=content.get("region_code"),
                    region_name=content.get("region_name"),
                    city=content.get("city"),
                    zip=content.get("zip"),
                    latitude=content.get("latitude"),
                    longitude=content.get("longitude"),
                    location=content.get("location"),
                )
                return Response({"message": f"IP {address} was saved to the database."})
            except Exception as e:
                return Response({"message": e})

    def get(self, request):
        address = request.GET.get("address")

        # Get specific Geolocalization
        if address:
            try:
                geolocalization = Geolocalization.objects.get(ip=address)
                serializer = GeolocalizationSerializer(geolocalization)
                return Response(serializer.data)
            except Exception as e:
                return Response(
                    {
                        "message": f"{e} Please provide a valid IP address in body parameters."
                    }
                )

        # Show list of all Geolocalizations
        else:
            geolocalizations = Geolocalization.objects.all()
            response = []
            [response.append(geo.ip) for geo in geolocalizations]
            return Response(response)

    def delete(self, request):
        address = request.GET.get("address")
        try:
            geolocalization = Geolocalization.objects.get(ip=address)
            geolocalization.delete()
        except Exception as e:
            return Response(
                {
                    "message": f"{e} Please provide a valid IP address in body parameters."
                }
            )
        return Response({"message": f"Geolocalization for IP {address} was removed."})
