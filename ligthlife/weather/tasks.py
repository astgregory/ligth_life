from smtplib import SMTPException

from celery import shared_task

from celery_singleton import Singleton
from django.core.mail import send_mail

from weather.models import WeatherAlarm


@shared_task(base=Singleton)
def send_weather_message(weather_alarm_id):
    try:
        weather_alarm = WeatherAlarm.objects.get(id=weather_alarm_id)
        message = weather_alarm.get_weather_data()
        send_mail(
            subject=f'Погода для города: {weather_alarm.city}',
            message=message,
            from_email='astgregory87@gmail.com',
            recipient_list=[weather_alarm.email],
        )
    except WeatherAlarm.DoesNotExist:
        print(f'Weather alarm с id {weather_alarm_id} не существует')
    except SMTPException as e:
        print(f'Ошибка при отправке email: {e}')
