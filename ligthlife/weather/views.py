from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

from .models import WeatherAlarm, Days
from .serializers import UserSerializer, WeatherAlarmSerializer, DaysSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DaysViewSet(viewsets.ModelViewSet):
    queryset = Days.objects.all()
    serializer_class = DaysSerializer


class WeatherAlarmViewSet(viewsets.ModelViewSet):
    queryset = WeatherAlarm.objects.all()
    serializer_class = WeatherAlarmSerializer
    permission_classes = (IsAuthenticated,)
