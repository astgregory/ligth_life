from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import WeatherAlarm, Message
from .serializers import UserSerializer, WeatherAlarmSerializer, MessageSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class WeatherAlarmViewSet(viewsets.ModelViewSet):
    serializer_class = WeatherAlarmSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return WeatherAlarm.objects.filter(user=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        weather_alarm_id = self.kwargs['weather_alarm_id']
        return Message.objects.filter(weather_alarm_id=weather_alarm_id)

    def perform_create(self, serializer):
        weather_alarm_id = self.kwargs['weather_alarm_id']
        weather_alarm = WeatherAlarm.objects.get(pk=weather_alarm_id)
        serializer.save(weather_alarm=weather_alarm)