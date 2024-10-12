import requests
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
        fields = ['day']


class WeatherAlarmSerializer(serializers.ModelSerializer):
    days = DaysSerializer(many=True)


    class Meta:
        model = WeatherAlarm
        fields = ['country', 'city', 'phone_number', 'email', 'time', 'time_zone', 'days', 'lat', 'lon']

    def create(self, validated_data):
        days_data = validated_data.pop('days')
        user = self.context['request'].user
        weather_alarm = WeatherAlarm.objects.create(user=user, **validated_data)

        for day_name in days_data:
            day, _ = Days.objects.get_or_create(day=day_name)
            weather_alarm.days.add(day)

        return weather_alarm
    #
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['days'] = [day.day for day in instance.days.all()]
    #     return representation


