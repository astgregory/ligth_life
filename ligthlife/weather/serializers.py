from rest_framework import serializers
from django.contrib.auth.models import User

from .models import WeatherAlarm, Days


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class DaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Days
        fields = ['id', 'day']


class WeatherAlarmSerializer(serializers.ModelSerializer):
    days = DaysSerializer(many=True, required=False)

    def create(self, validated_data):
        days_data = validated_data.pop('days', [])
        user = self.context['request'].user
        weather_alarm = WeatherAlarm.objects.create(user=user, **validated_data)

        for day_data in days_data:
            day, created = Days.objects.get_or_create(day=day_data['day'])
            weather_alarm.days.add(day)

        return weather_alarm

    class Meta:
        model = WeatherAlarm
        fields = ['country', 'city', 'phone_number', 'email', 'time', 'time_zone', 'days', 'lat', 'lon']
