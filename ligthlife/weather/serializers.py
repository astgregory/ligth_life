from django.db import IntegrityError
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

    def create(self, validated_data):
        return Days.objects.create(validated_data)


class WeatherAlarmSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    days = DaysSerializer(many=True, read_only=False)
    time = serializers.TimeField()

    class Meta:
        model = WeatherAlarm
        fields = ('id', 'user', 'country', 'city', 'phone_number', 'email', 'time', 'time_zone', 'days', 'lat', 'lon')

        def create(self, validated_data):
            weather_alarm = WeatherAlarm.objects.create(user=self.context['request'].user, **validated_data)
            return weather_alarm

        def update(self, instance, validated_data):
            return super().update(instance, validated_data)
#
# class WeatherAlarmSerializer(serializers.ModelSerializer):
#     user = UserSerializer(many=True, read_only=True)
#     days = DaysSerializer(read_only=True, many=True)
#
#     class Meta:
#         model = WeatherAlarm
#         fields = ['id', 'user', 'country', 'city', 'phone_number', 'email', 'days', 'time', 'lat', 'lon', 'time_zone']


