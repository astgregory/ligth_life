from datetime import time

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from weather.models import WeatherAlarm, Days
from weather.serializers import WeatherAlarmSerializer, DaysSerializer, UserSerializer


class WeatherAlarmSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.days = Days.objects.create(day='Понедельник')
        self.weather_alarm = WeatherAlarm.objects.create(user=self.user, country='US', city='New York',
                                                         phone_number='1234567890', email='test@example.com',
                                                         time=time(hour=12, minute=0), lat='40.712728',
                                                         lon='-74.006015',
                                                         time_zone='America/New_York')
        self.weather_alarm.days.set([self.days])
        self.client = APIClient()

    def test_serializer_fields(self):
        serializer = WeatherAlarmSerializer(instance=self.weather_alarm)
        data = serializer.data
        self.assertEqual(set(data.keys()),
                         {'country', 'city', 'phone_number', 'email', 'days', 'time', 'lat', 'lon',
                          'time_zone'})


        self.assertEqual(data['days'], [{'id': self.days.id, 'day': 'Понедельник'}])
        self.assertEqual(data['country'], 'US')
        self.assertEqual(data['city'], 'New York')
        self.assertEqual(data['phone_number'], '1234567890')
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['time'], '12:00:00')
        self.assertEqual(data['lat'], '40.712728')
        self.assertEqual(data['lon'], '-74.006015')
        self.assertEqual(data['time_zone'], 'America/New_York')


class DaysSerializerTest(TestCase):
    def setUp(self):
        self.days = Days.objects.create(day='Четверг')
        self.client = APIClient()

    def test_serializer_fields(self):
        serializer = DaysSerializer(instance=self.days)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'id','day'})
        self.assertEqual(data['day'], self.days.day)
        self.assertEqual(data['id'], self.days.id)


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()

    def test_serializer_fields(self):
        serializer = UserSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'id', 'username'})
        self.assertEqual(data['username'], 'testuser')

