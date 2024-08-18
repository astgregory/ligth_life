from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import WeatherAlarm
from .serializers import UserSerializer, WeatherAlarmSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WeatherAlarmViewSet(viewsets.ModelViewSet):
    queryset = WeatherAlarm.objects.all()
    serializer_class = WeatherAlarmSerializer


