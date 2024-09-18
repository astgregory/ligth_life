from datetime import time

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from unittest.mock import patch
from weather.models import WeatherAlarm, Days
from django.contrib.auth import get_user_model

from weather.serializers import WeatherAlarmSerializer

User = get_user_model()


class UserApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_user(self):
        url = reverse('user-list')
        response = self.client.post(url, {'username': 'newuser', 'password': 'newpassword'}, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_user(self):
        url = reverse('user-detail', args=[self.user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'testuser')


class WeatherAlarmApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.days = Days.objects.create(day='1')
        self.weather_alarm = WeatherAlarm.objects.create(
            user=self.user,
            country='RU',
            city='Astrakhan',
            phone_number='+79991234567',
            email='astgregory@bk.ru',
            time=time(hour=12, minute=30),
            time_zone='Europe/Astrakhan'
        )
        self.weather_alarm.days.set([self.days])

    def test_create_alarm(self):
        user_1 = User.objects.create_user(username='test_user', password='testpassword')
        # days = Days.objects.create(day='2')
        weather_alarm = {
                "country": "RU",
                "city": "Москва",
                "phone_number": "79275826417",
                "email": "test2@bk.ru",
                "time": '11:34:24',
                "time_zone": 'Europe/Moscow',
                "days": [
                        {
                            "day": "2"
                        },
                        {
                            "day": "5"
                        }
                    ],
                "lat": "55.750446",
                "lon": "37.617494"
            }

        serializer = WeatherAlarmSerializer(weather_alarm)
        print(f"Serialized data: {serializer.data}")
        serializer_data = WeatherAlarmSerializer(weather_alarm).data
        url = reverse('weather-alarm-list')
        print(f"Request data: {serializer_data}")
        response = self.client.post(url, serializer_data, format='json')
        print(f"Response data: {response.data}")

        self.assertEqual(response.status_code, 201)

    # def test_create_alarm(self):
    #     user_1 = User.objects.create_user(username='test_user', password='testpassword')
    #     weather_alarm_create = WeatherAlarm.objects.create(user=user_1, country='US', city='New York',
    #                                                      phone_number='1234567890', email='test@example.com',
    #                                                      time=time(hour=12, minute=0), lat='40.712728',
    #                                                      lon='-74.006015',
    #                                                      time_zone='America/New_York')
    #     weather_alarm_create.days.set([self.days])
    #     print(self.weather_alarm.days)
    #     print(weather_alarm_create.id)
    #     serializer_data = WeatherAlarmSerializer(weather_alarm_create).data
    #     url = reverse('weather-alarm-list')
    #     response = self.client.post(url, serializer_data, format='json')
    #
    #
    #
    #     self.assertEqual(response.status_code, 201)


    def test_get_alarm(self):
        url = reverse('weather-alarm-detail', args=[self.weather_alarm.id])
        response = self.client.get(url)
        serializer_data = WeatherAlarmSerializer(self.weather_alarm).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer_data)

# {
#     "country": "RU",
#     "city": "Москва",
#     "phone_number": "79275826419",
#     "email": "test2@bk.ru",
#     "time": "11:34:24",
#     "time_zone": "Europe/Moscow",
#     "days": [
#             {
#                 "day": "3"
#             },
#             {
#                 "day": "6"
#             }
#         ],
#     "lat": "55.750446",
#     "lon": "37.617494"
# }