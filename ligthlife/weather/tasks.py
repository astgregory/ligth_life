import requests
import json
from django.utils.log import logging
from smtplib import SMTPException
from celery import shared_task
from celery_singleton import Singleton
from django.core.mail import send_mail

from weather.models import WeatherAlarm
from celery.exceptions import SoftTimeLimitExceeded
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from requests.exceptions import RequestException
from django_celery_beat.models import CrontabSchedule, PeriodicTask

logger = logging.getLogger(__name__)


@shared_task(base=Singleton)
def send_weather_message(weather_alarm_id):
    try:
        weather_alarm = WeatherAlarm.objects.get(id=weather_alarm_id)
        message = get_weather_data(weather_alarm_id)
        send_mail(
            subject=f'Погода для города: {weather_alarm.city}',
            message=message,
            from_email='astgregory87@gmail.com',
            recipient_list=[weather_alarm.email],
        )
    except WeatherAlarm.DoesNotExist:
        logger.error(f'Weather alarm с id {weather_alarm_id} не существует')
    except SMTPException as e:
        logger.error(f'Ошибка при отправке email: {e}')


@shared_task(base=Singleton)
def set_latitude_and_longitude(weather_alarm_id):
    try:
        with transaction.atomic():
            weather_alarm = WeatherAlarm.objects.select_for_update().get(id=weather_alarm_id)
            api_key = 'e796fce1a1eec7055ae4f1a3f2637930'
            url = f"https://ru.api.openweathermap.org/geo/1.0/direct?q={weather_alarm.city},{weather_alarm.country}&appid={api_key}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if data:
                    weather_alarm.lat = data[0]['lat']
                    weather_alarm.lon = data[0]['lon']
                    weather_alarm.save(flag=False)
                    set_periodic_task_send_weather_message(weather_alarm.id)

            else:
                logger.error(
                    f'Не удалось получить данные о местоположении для города {weather_alarm.city}, страны {weather_alarm.country}. Код состояния: {response.status_code}')

    except ObjectDoesNotExist:
        logger.error(f'Weather alarm с id {weather_alarm_id} не существует')
    except SoftTimeLimitExceeded:
        logger.error(f'Превышено время выполнения задачи set_latitude_and_longitude({weather_alarm_id})')
    except RequestException as e:
        logger.error(
            f'Не удалось получить данные о местоположении для города {weather_alarm.city}, страны {weather_alarm.country}. Ошибка: {e}')


def set_periodic_task_send_weather_message(weather_alarm_id):
    crontab_days = {
        'Понедельник': '1',
        'Вторник': '2',
        'Среда': '3',
        'Четверг': '4',
        'Пятница': '5',
        'Суббота': '6',
        'Воскресенье': '0',
    }
    weather_alarm = WeatherAlarm.objects.get(id=weather_alarm_id)
    days_list = [crontab_days[day.day] for day in weather_alarm.days.all()]
    try:
        task = PeriodicTask.objects.get(name=f'Send weather message task for "{weather_alarm.user.username.title()}"')
        shedule = task.crontab
        shedule.minute = weather_alarm.time.minute
        shedule.hour = weather_alarm.time.hour
        shedule.day_of_week = ','.join(days_list)
        shedule.day_of_month = '*'
        shedule.month_of_year = '*'
        shedule.timezone = weather_alarm.time_zone

        shedule.save()


    except PeriodicTask.DoesNotExist:
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=weather_alarm.time.minute,
            hour=weather_alarm.time.hour,
            day_of_week=','.join(days_list),
            day_of_month='*',
            month_of_year='*',
            timezone=weather_alarm.time_zone
        )

        task = PeriodicTask.objects.create(
            name=f'Send weather message task for "{weather_alarm.user.username.title()}"',
            task='weather.tasks.send_weather_message',
            crontab=schedule,
            args=json.dumps([weather_alarm.id])
        )
        task.save()


def get_weather_data(weather_alarm_id):
    weather_alarm = WeatherAlarm.objects.get(id=weather_alarm_id)
    api_key = 'e796fce1a1eec7055ae4f1a3f2637930'
    url = f'https://ru.api.openweathermap.org/data/2.5/weather?lat={weather_alarm.lat}&lon={weather_alarm.lon}&appid={api_key}&lang={weather_alarm.country}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        if 'weather' in weather_data:
            return (f'Погода на улице: {weather_data["weather"][0]["description"]}\n'
                    f'Температура: {weather_data["main"]["temp"]} градусов по Цельсию, но ощущается как {weather_data["main"]["feels_like"]} градусов\n'
                    f'Влажность воздуха: {weather_data["main"]["humidity"]} %\n'
                    f'Скорость ветра: {weather_data["wind"]["speed"]} м/с\n'
                    f'Облачность: {weather_data["clouds"]["all"]} %\n')
        else:
            return 'Ошибка получения данных о погоде: API вернуло пустой список weather'
    else:
        return f'Ошибка получения данных о погоде: {response.status_code}'