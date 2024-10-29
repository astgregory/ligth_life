from rest_framework import serializers
from django.contrib.auth.models import User

from .models import WeatherAlarm, Days


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


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

    def update(self, instance, validated_data):
        days_data = validated_data.pop('days', None)

        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email = validated_data.get('email', instance.email)
        instance.time = validated_data.get('time', instance.time)
        instance.time_zone = validated_data.get('time_zone', instance.time_zone)
        instance.lat = validated_data.get('lat', instance.lat)
        instance.lon = validated_data.get('lon', instance.lon)
        instance.save()

        if days_data is not None:
            instance.days.clear()
            for day_data in days_data:
                day, created = Days.objects.get_or_create(day=day_data['day'])
                instance.days.add(day)

        return instance

    class Meta:
        model = WeatherAlarm
        fields = ['country', 'city', 'phone_number', 'email', 'time', 'time_zone', 'days', 'lat', 'lon']
