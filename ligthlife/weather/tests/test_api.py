from datetime import time

from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User

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

    def test_create_alarm(self):
        user_1 = User.objects.create_user(username='test_user', password='testpassword')
        url = reverse('weather-alarm-list')
        weather_alarm_data = {
            "country": "RU",
            "city": "Москва",
            "phone_number": "+79275826417",
            "email": "test2@bk.ru",
            "time": '11:34:24',
            "time_zone": 'Europe/Moscow',
            "days": [
                {
                    "day": "Понедельник"
                },
                {
                    "day": "Среда"
                }],
            "lat": "55.750446",
            "lon": "37.617494"
        }
        self.client.login(username='test_user', password='testpassword')

        response = self.client.post(url, weather_alarm_data, format='json')

        self.assertEqual(response.status_code, 201)

        self.assertTrue(WeatherAlarm.objects.filter(email='test2@bk.ru').exists())

        created_alarm = WeatherAlarm.objects.get(email='test2@bk.ru')
        self.assertEqual(created_alarm.country, weather_alarm_data['country'])
        self.assertEqual(created_alarm.city, weather_alarm_data['city'])
        self.assertEqual(created_alarm.phone_number, weather_alarm_data['phone_number'])
        self.assertEqual(created_alarm.email, weather_alarm_data['email'])
        self.assertEqual(created_alarm.time.strftime('%H:%M:%S'), weather_alarm_data['time'])
        self.assertEqual(created_alarm.time_zone, weather_alarm_data['time_zone'])
        self.assertEqual(str(created_alarm.lat), weather_alarm_data['lat'])
        self.assertEqual(str(created_alarm.lon), weather_alarm_data['lon'])
        self.assertTrue(created_alarm.days.filter(day='Понедельник').exists())
        self.assertTrue(created_alarm.days.filter(day='Среда').exists())

    def test_get_alarm(self):
        url = reverse('weather-alarm-detail', args=[self.weather_alarm.id])
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(url)
        serializer_data = WeatherAlarmSerializer(self.weather_alarm).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer_data)

    def test_update_alarm(self):
        self.client.login(username='testuser', password='testpassword')

        url = reverse('weather-alarm-detail', args=[self.weather_alarm.id])
        updated_data = {
            "country": "RU",
            "city": "Нижний Новгород",
            "phone_number": "+79275826417",
            "email": "updated_test2@bk.ru",
            "time": '15:00:00',
            "time_zone": 'Europe/Moscow',
            "days": [
                {"day": "Вторник"},
                {"day": "Четверг"}
            ],
            "lat": "56.296503",
            "lon": "43.936059"
        }

        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, 200)

        updated_alarm = WeatherAlarm.objects.get(id=self.weather_alarm.id)
        self.assertEqual(updated_alarm.city, updated_data['city'])
        self.assertEqual(updated_alarm.email, updated_data['email'])
        self.assertTrue(updated_alarm.days.filter(day='Вторник').exists())
        self.assertTrue(updated_alarm.days.filter(day='Четверг').exists())

    def test_delete_alarm(self):
        self.client.login(username='testuser', password='testpassword')

        url = reverse('weather-alarm-detail', args=[self.weather_alarm.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)  # Код 204 - No Content

        self.assertFalse(WeatherAlarm.objects.filter(id=self.weather_alarm.id).exists())
