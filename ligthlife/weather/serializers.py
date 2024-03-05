from rest_framework import serializers
from django.contrib.auth.models import User
from .models import WeatherAlarm, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class WeatherAlarmSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = WeatherAlarm
        fields = ['id', 'user', 'country', 'city']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'weather_alarm', 'text', 'status', 'timestamp']