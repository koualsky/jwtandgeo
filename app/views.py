from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer


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
