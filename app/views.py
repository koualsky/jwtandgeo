from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from django.conf import settings
import socket
import requests
import json
import re
from .serializers import UserSerializer
from .models import Geolocalization


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        AllowAny
    ]
    serializer_class = UserSerializer


class GeolocalizationView(APIView):

    def post(self, request):
        address = request.POST.get('address')
        if not address:
            return Response({"message": f'Please provide a valid ip address in body parameters.'})
        is_ip = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", address)
        if not is_ip:
            try:
                address = socket.gethostbyname(address)
            except Exception as e:
                return Response({"message": f'{e}. Please provide a valid ip address in body parameters.'})
        if address:
            r = requests.get(f'http://api.ipstack.com/{address}?access_key={settings.GEOLOCALIZATION_KEY}&format=1')
            content = json.loads(r.text)
            obj, created = Geolocalization.objects.get_or_create(
                ip=content.get('ip'),
                type=content.get('type'),
                continent_code=content.get('continent_code'),
                continent_name=content.get('continent_name'),
                country_code=content.get('country_code'),
                country_name=content.get('country_name'),
                region_code=content.get('region_code'),
                region_name=content.get('region_name'),
                city=content.get('city'),
                zip=content.get('zip'),
                latitude=content.get('latitude'),
                longitude=content.get('longitude'),
                location=content.get('location'),
            )
            if created:
                return Response({"message": f"IP {address} was saved to the database."})
            else:
                return Response({"message": f"Geolocalization with this ip ({address}) already exists in the database."})
        else:
            return Response({"message": f'Please provide a valid ip address in body parameters.'})

    def get(self, request):
        content = {"message": "Response for get :)"}
        return Response(content)

    def delete(self, request):
        pk = request.POST.get('pk')
        content = {"message": f"PK: {pk} was deleted!"}
        return Response(content)
