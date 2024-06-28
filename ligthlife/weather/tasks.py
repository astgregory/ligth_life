# from django.core.mail import send_mail
# from .models import WeatherAlarm
from celery import shared_task
import datetime

from celery_singleton import Singleton


@shared_task(base=Singleton)
def send_weather_message():
    now = datetime.datetime.now()
    print(f"Current time: {now}")

    # for weather_alarm in WeatherAlarm.objects.all():
    #     if weather_alarm.is_due(now):
    #         message = weather_alarm.get_weather_data()
    #         subject = f'Погода для города: {weather_alarm.city}'
    #         send_mail(
    #             subject=subject,
    #             message=message,
    #             from_email='astgregory87@gmail.com',
    #             recipient_list=[weather_alarm.email],
    #         )
