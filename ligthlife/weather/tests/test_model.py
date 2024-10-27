from datetime import time

from django.contrib.auth.models import User
from django.test import TestCase
from unittest.mock import patch

from weather.models import WeatherAlarm, Days
from rest_framework.test import APIClient


class WeatherAlarmModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.days = Days.objects.create(day='Понедельник')
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
        self.client = APIClient()

    @patch('requests.get')
    def test_create_weather_alarm(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{
            'lat': 46.349831,
            'lon': 48.032620
        }]
        weather_alarm = self.weather_alarm
        latitude_info = mock_get.return_value.json()[0]
        weather_alarm.lat = latitude_info['lat']
        weather_alarm.lon = latitude_info['lon']
        weather_alarm.save()
        weather_alarm = WeatherAlarm.objects.get(id=self.weather_alarm.id)

        expected_data = {
            "id": weather_alarm.id,
            "user": {
                "id": self.user.id,
                "username": 'test_user',
                "email": ""
            },
            "country": "RU",
            "city": "Astrakhan",
            "phone_number": '+79991234567',
            "email": "astgregory@bk.ru",
            "days": [
                {
                    "day": 'Понедельник',
                }
            ],
            "time": "12:30:00",
            "lat": '46.349831',
            "lon": '48.032620',
            "time_zone": 'Europe/Astrakhan'
        }

        self.assertEqual(weather_alarm.id, expected_data['id'])
        self.assertEqual(weather_alarm.user.id, expected_data['user']['id'])
        self.assertEqual(weather_alarm.country, expected_data['country'])
        self.assertEqual(weather_alarm.city, expected_data['city'])
        self.assertEqual(weather_alarm.phone_number, expected_data['phone_number'])
        self.assertEqual(weather_alarm.email, expected_data['email'])
        self.assertEqual(weather_alarm.time.strftime('%H:%M:%S'), expected_data['time'])
        self.assertEqual(str(weather_alarm.lat), str(expected_data['lat']))
        self.assertEqual(str(weather_alarm.lon), str(expected_data['lon']))
        self.assertEqual(weather_alarm.time_zone, expected_data['time_zone'])
        self.assertTrue(weather_alarm.days.filter(id=self.days.id).exists())
