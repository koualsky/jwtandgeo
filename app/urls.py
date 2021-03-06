from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("hello/", views.HelloView.as_view(), name="hello"),
    path(
        "geolocalization/", views.GeolocalizationView.as_view(), name="geolocalization"
    ),
]
