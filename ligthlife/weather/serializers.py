from rest_framework import serializers
from django.contrib.auth.models import User

from .models import WeatherAlarm, Days


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class DaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Days
        fields = ['day']


class WeatherAlarmSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    days = DaysSerializer(many=True)

    class Meta:
        model = WeatherAlarm
        fields = ['id', 'user', 'country', 'city', 'phone_number', 'email', 'days', 'time', 'lat', 'lon', 'time_zone']


