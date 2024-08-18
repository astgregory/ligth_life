from django.test import TestCase
from .models import Days
from .serializers import WeatherAlarmSerializer
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import WeatherAlarm


class WeatherAlarmSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.days = Days.objects.create(day='Monday')
        self.weather_alarm = WeatherAlarm.objects.create(user=self.user, country='US', city='New York',
                                                         phone_number='1234567890', email='test@example.com',
                                                         days=self.days, time='12:00', lat='40.7128', lon='74.0060',
                                                         time_zone='America/New_York')
        self.client = APIClient()

    def test_serializer_fields(self):
        serializer = WeatherAlarmSerializer(instance=self.weather_alarm)
        data = serializer.data
        self.assertEqual(set(data.keys()),
                         {'id', 'user', 'country', 'city', 'phone_number', 'email', 'days', 'time', 'lat', 'lon',
                          'time_zone'})
        self.assertEqual(data['user'], {'id': self.user.id, 'username': 'testuser', 'email': ''})
        self.assertEqual(data['days'], [{'day': 'Monday'}])


class UserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_user(self):
        response = self.client.post('/api/users/', {'username': 'newuser', 'password': 'newpassword'}, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_user(self):
        response = self.client.get('/api/users/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'testuser')


class WeatherAlarmApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.alarm = WeatherAlarm.objects.create(user=self.user, city='Moscow', temperature=10)

    def test_create_alarm(self):
        response = self.client.post('/api/alarms/', {'user': self.user.id, 'city': 'St. Petersburg', 'temperature': 20},
                                    format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_alarm(self):
        response = self.client.get('/api/alarms/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['city'], 'Moscow')
        self.assertEqual(response.data['temperature'], 10)
